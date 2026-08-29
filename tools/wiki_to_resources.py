#!/usr/bin/env python3
"""wiki_to_resources — pipeline wiki → datos (ANDAMIO / scaffold).

Lee las fichas YAML de `docs/WIKI.md` (fuente canónica, ver CLAUDE.md) y las
convierte en recursos de datos bajo `data/`. También puede regenerar el índice
navegable de la wiki (`docs/wiki/README.md`) para que la navegación nunca
quede desincronizada del contenido canónico.

ESTADO: andamio. Lee y valida todo lo que hay hoy y emite JSON completo;
el escritor `.tres` es un esqueleto (necesita las clases Resource de C# que
todavía no existen — ver TECH §2 y el backlog en `tasks/`).

Principios (no romper al extender):
  1. La wiki es la fuente canónica. Este script NUNCA escribe en docs/WIKI.md.
  2. Los valores `TBD` se propagan tal cual. Este script no inventa balance.
  3. Sin dependencias externas: el parser YAML es un subconjunto tolerante
     (PyYAML se usa si está disponible, con fallback automático).

Uso:
    python3 tools/wiki_to_resources.py --check            # valida, no escribe
    python3 tools/wiki_to_resources.py                    # genera data/**/*.json
    python3 tools/wiki_to_resources.py --only peon        # una sola ficha
    python3 tools/wiki_to_resources.py --format tres      # .tres (EXPERIMENTAL)
    python3 tools/wiki_to_resources.py --emit-index       # docs/wiki/README.md
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
WIKI_PATH = REPO_ROOT / "docs" / "WIKI.md"
DATA_DIR = REPO_ROOT / "data"
WIKI_INDEX_PATH = REPO_ROOT / "docs" / "wiki" / "README.md"

#: `tipo` de la ficha → subcarpeta de data/. Extender acá cuando la wiki gane
#: un esquema de ficha nuevo (ver el backlog de WIKI §7).
TIPO_TO_DIR = {
    "unidad_jugador": "units",
    "enemigo": "enemies",
    "arma": "weapons",
    "edificio": "buildings",
    "oleada": "waves",
    # `recurso` entró con la wiki v0.2: el ganado dejó de ser "comida pasiva" y
    # pasó a ser una cadena (pasto → vaca → comida) con fichas propias.
    "recurso": "resources",
}

#: `tipo` → clase Resource de C# que consumirá el .tres. Todavía no existen
#: (TECH §2 las planifica); el escritor .tres las referencia como placeholder.
TIPO_TO_RESOURCE_SCRIPT = {
    "unidad_jugador": "res://src/Units/UnitData.cs",
    "enemigo": "res://src/Enemies/EnemyData.cs",
    # Las armas son el árbol tecnológico (GDD §8.1), que en TECH §2 vive en Tech/.
    "arma": "res://src/Tech/WeaponData.cs",
    "edificio": "res://src/Buildings/BuildingData.cs",
    # La oleada la consume el WaveDirector, que en TECH §2 vive en Enemies/.
    "oleada": "res://src/Enemies/WaveData.cs",
    # Los recursos los consume el ResourceLedger (TECH §2, Economy/).
    "recurso": "res://src/Economy/ResourceData.cs",
}

TBD = "TBD"


# --------------------------------------------------------------------------
# Extracción de bloques
# --------------------------------------------------------------------------

FENCE_RE = re.compile(r"^```(\w*)\s*$")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*#*$")


class Block:
    """Un bloque ```yaml de la wiki, con el contexto de encabezados que lo ubica."""

    def __init__(self, text: str, line: int, headings: dict[int, str]):
        self.text = text
        self.line = line
        self.headings = dict(headings)

    @property
    def section(self) -> str:
        """El encabezado más profundo que contiene al bloque (ej. '1.1 peon')."""
        if not self.headings:
            return ""
        return self.headings[max(self.headings)]

    @property
    def breadcrumb(self) -> str:
        return " › ".join(self.headings[lvl] for lvl in sorted(self.headings))


def extract_yaml_blocks(markdown: str) -> list[Block]:
    """Devuelve los bloques ```yaml del markdown, en orden de aparición."""
    blocks: list[Block] = []
    headings: dict[int, str] = {}
    buf: list[str] | None = None
    buf_start = 0

    for lineno, raw in enumerate(markdown.splitlines(), start=1):
        fence = FENCE_RE.match(raw)
        if fence:
            if buf is None:
                if fence.group(1) == "yaml":
                    buf, buf_start = [], lineno + 1
            else:
                blocks.append(Block("\n".join(buf), buf_start, headings))
                buf = None
            continue

        if buf is not None:
            buf.append(raw)
            continue

        heading = HEADING_RE.match(raw)
        if heading:
            level = len(heading.group(1))
            headings = {lvl: t for lvl, t in headings.items() if lvl < level}
            headings[level] = heading.group(2)

    if buf is not None:
        # Fence sin cerrar: la wiki está truncada o mal formada.
        raise ValueError(
            f"bloque ```yaml sin cerrar que empieza en la línea {buf_start} "
            f"— ¿docs/WIKI.md está truncado?"
        )
    return blocks


# --------------------------------------------------------------------------
# Parser YAML (subconjunto tolerante, sin dependencias)
# --------------------------------------------------------------------------


def _split_top_level(s: str) -> list[str]:
    """Parte por comas ignorando las que están dentro de (), [], {} o comillas."""
    parts, depth, quote, cur = [], 0, "", []
    for ch in s:
        if quote:
            cur.append(ch)
            if ch == quote:
                quote = ""
            continue
        if ch in "\"'":
            quote = ch
            cur.append(ch)
        elif ch in "([{":
            depth += 1
            cur.append(ch)
        elif ch in ")]}":
            depth -= 1
            cur.append(ch)
        elif ch == "," and depth == 0:
            parts.append("".join(cur).strip())
            cur = []
        else:
            cur.append(ch)
    tail = "".join(cur).strip()
    if tail:
        parts.append(tail)
    return parts


def _strip_comment(value: str) -> str:
    """Quita el comentario `# ...` de cola. No toca `#` dentro de comillas.

    Un valor que es *solo* comentario (las plantillas de esquema en WIKI §0,
    ej. `id:            # snake_case canónico`) queda vacío — que es como se
    distingue una plantilla de una ficha real.
    """
    if value.startswith(("'", '"')):
        return value
    if value.startswith("#"):
        return ""
    return re.split(r"\s+#\s", value, maxsplit=1)[0].rstrip()


def _coerce(value: str):
    v = value.strip()
    if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
        return v[1:-1]
    if v.startswith("{") and v.endswith("}"):
        out = {}
        for item in _split_top_level(v[1:-1]):
            if ":" in item:
                k, _, val = item.partition(":")
                out[k.strip()] = _coerce(val)
            elif item:
                out[item] = None
        return out
    if v.startswith("[") and v.endswith("]"):
        return [_coerce(i) for i in _split_top_level(v[1:-1])]
    if v in ("true", "false"):
        return v == "true"
    if re.fullmatch(r"-?\d+", v):
        return int(v)
    return v


def parse_ficha(text: str) -> dict:
    """Parsea una ficha a dict.

    Usa PyYAML si está instalado y logra parsear; si no (o si falla, porque
    algunas fichas contienen `: ` dentro de escalares planos), cae al parser
    tolerante línea-a-línea. Ambos caminos devuelven la misma forma.
    """
    try:  # camino preferente, si el entorno lo tiene
        import yaml  # type: ignore

        parsed = yaml.safe_load(text)
        if isinstance(parsed, dict):
            return parsed
    except Exception:
        pass
    return _parse_ficha_tolerant(text)


def _parse_ficha_tolerant(text: str) -> dict:
    out: dict = {}
    key = None
    for raw in text.splitlines():
        line = raw.rstrip()
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line.startswith((" ", "\t")) and key is not None:
            # Continuación de un valor multilínea: se concatena como texto.
            out[key] = f"{out[key]} {line.strip()}".strip()
            continue
        m = re.match(r"^([A-Za-z_][\w]*)\s*:\s*(.*)$", line)
        if not m:
            continue
        key, value = m.group(1), _strip_comment(m.group(2))
        out[key] = _coerce(value) if value else ""
    return out


# --------------------------------------------------------------------------
# Carga y validación
# --------------------------------------------------------------------------

#: Campos que toda ficha debe traer, por tipo (ver WIKI §0).
REQUIRED_FIELDS = {
    "unidad_jugador": ["id", "nombre", "tipo", "rol", "estado"],
    "enemigo": ["id", "nombre", "tipo", "categoria", "que_roba", "contramedida", "estado"],
    "arma": ["id", "nombre", "tipo", "tier", "montaje", "efecto", "estado"],
    "edificio": ["id", "nombre", "tipo", "funcion", "slot", "estado"],
    "oleada": ["id", "nombre", "tipo", "noche", "fase_lunar", "estado"],
    "recurso": ["id", "nombre", "tipo", "clase", "fuente", "estado"],
}


class Ficha:
    def __init__(self, data: dict, block: Block):
        self.data = data
        self.block = block

    @property
    def id(self) -> str:
        return str(self.data.get("id", ""))

    @property
    def tipo(self) -> str:
        return str(self.data.get("tipo", ""))

    @property
    def estado(self) -> str:
        return str(self.data.get("estado", ""))

    def tbd_fields(self) -> list[str]:
        """Rutas de campo (`stats.vida`) cuyo valor es TBD. Nunca se rellenan."""
        found = []

        def walk(value, path):
            if isinstance(value, dict):
                for k, v in value.items():
                    walk(v, f"{path}.{k}" if path else str(k))
            elif isinstance(value, list):
                for i, v in enumerate(value):
                    walk(v, f"{path}[{i}]")
            elif isinstance(value, str) and TBD in value:
                found.append(path)

        walk(self.data, "")
        return found

    def problems(self) -> list[str]:
        missing = [
            f for f in REQUIRED_FIELDS.get(self.tipo, ["id", "tipo"])
            if not self.data.get(f)
        ]
        return [f"falta el campo requerido `{f}`" for f in missing]

    def to_record(self, wiki_rel: str) -> dict:
        record = dict(self.data)
        record["_meta"] = {
            "generated_by": "tools/wiki_to_resources.py",
            "source": wiki_rel,
            "source_line": self.block.line,
            "section": self.block.section,
            "tbd_fields": self.tbd_fields(),
        }
        return record


def load_fichas(wiki_path: Path) -> tuple[list[Ficha], list[str]]:
    """Devuelve (fichas, avisos). Los bloques de esquema de §0 se descartan."""
    markdown = wiki_path.read_text(encoding="utf-8")
    warnings: list[str] = []
    fichas: list[Ficha] = []
    seen: dict[str, Ficha] = {}

    for block in extract_yaml_blocks(markdown):
        data = parse_ficha(block.text)
        entity_id = str(data.get("id", "")).strip()
        if not entity_id:
            # Plantilla de esquema (WIKI §0), no una entidad.
            continue
        ficha = Ficha(data, block)
        if entity_id in seen:
            warnings.append(
                f"id duplicado `{entity_id}` (líneas {seen[entity_id].block.line} "
                f"y {block.line})"
            )
            continue
        if ficha.tipo not in TIPO_TO_DIR:
            warnings.append(
                f"`{entity_id}` (línea {block.line}): tipo `{ficha.tipo}` sin "
                f"carpeta de destino — se omite"
            )
            continue
        seen[entity_id] = ficha
        fichas.append(ficha)

    # Comprobación de integridad frente al final del documento: si la wiki está
    # truncada, el último bloque no llega y conviene que se note.
    truncation = detect_truncation(markdown)
    if truncation:
        warnings.append(f"docs/WIKI.md {truncation} — posible truncamiento")
    return fichas, warnings


def detect_truncation(markdown: str) -> str | None:
    """Describe por qué el documento parece cortado a mitad, o None si cierra bien.

    Busca señales estructurales de una escritura interrumpida — no de estilo de
    redacción. El corte real del commit inicial dejó `## 13. Preguntas Ab` en el
    GDD y `| nucleo_ganadero | Único | El G` en la wiki: una fila de tabla sin
    cerrar, un encabezado sin cuerpo y, en ambos casos, sin salto de línea final.
    """
    if not markdown:
        return "está vacío"
    if not markdown.endswith("\n"):
        return "no termina en salto de línea"

    lines = [ln for ln in markdown.splitlines() if ln.strip()]
    if not lines:
        return "no tiene contenido"
    last = lines[-1].strip()

    if last.startswith("|") and not last.endswith("|"):
        return "termina en una fila de tabla sin cerrar"
    if HEADING_RE.match(last):
        return "termina en un encabezado sin cuerpo"
    return None


# --------------------------------------------------------------------------
# Escritores
# --------------------------------------------------------------------------


def write_json(ficha: Ficha, out_dir: Path, wiki_rel: str) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"{ficha.id}.json"
    path.write_text(
        json.dumps(ficha.to_record(wiki_rel), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return path


def _tres_value(value) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int):
        return str(value)
    if isinstance(value, list):
        return "[" + ", ".join(_tres_value(v) for v in value) + "]"
    if isinstance(value, dict):
        inner = ", ".join(f'"{k}": {_tres_value(v)}' for k, v in value.items())
        return "{" + inner + "}"
    return '"' + str(value).replace("\\", "\\\\").replace('"', '\\"') + '"'


def write_tres(ficha: Ficha, out_dir: Path) -> Path:
    """ANDAMIO: escribe un .tres de Godot 4.

    TBD: el `script_class` y el ExtResource apuntan a clases C# que todavía no
    existen (TECH §2). Hasta que existan, Godot no podrá cargar estos recursos.
    Ver el backlog para el ticket que cierra esto.
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    script_path = TIPO_TO_RESOURCE_SCRIPT[ficha.tipo]
    class_name = Path(script_path).stem

    lines = [
        f'[gd_resource type="Resource" script_class="{class_name}" '
        f"load_steps=2 format=3]",
        "",
        f'[ext_resource type="Script" path="{script_path}" id="1_script"]',
        "",
        "[resource]",
        'script = ExtResource("1_script")',
    ]
    for key, value in ficha.data.items():
        lines.append(f"{key} = {_tres_value(value)}")
    lines.append("")

    path = out_dir / f"{ficha.id}.tres"
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def write_manifest(fichas: list[Ficha], wiki_rel: str) -> Path:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    manifest = {
        "generated_by": "tools/wiki_to_resources.py",
        "source": wiki_rel,
        "count": len(fichas),
        "entities": [
            {
                "id": f.id,
                "nombre": f.data.get("nombre", ""),
                "tipo": f.tipo,
                "categoria": f.data.get("categoria"),
                "estado": f.estado,
                "path": f"{TIPO_TO_DIR[f.tipo]}/{f.id}.json",
                "tbd_fields": f.tbd_fields(),
            }
            for f in fichas
        ],
    }
    path = DATA_DIR / "manifest.json"
    path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return path


# --------------------------------------------------------------------------
# Índice navegable de la wiki
# --------------------------------------------------------------------------


def slug(heading: str) -> str:
    """Ancla estilo GitHub para un encabezado markdown."""
    s = heading.strip().lower()
    s = re.sub(r"[^\w\s-]", "", s, flags=re.UNICODE)
    return s.replace(" ", "-")


INDEX_PREAMBLE = """# Wiki de Entidades — índice navegable

> **Este archivo es generado.** Se produce con
> `python3 tools/wiki_to_resources.py --emit-index`.
> La **fuente canónica** es [`docs/WIKI.md`](../WIKI.md): editá las fichas ahí
> y regenerá este índice. No edites este archivo a mano.

Documentos hermanos: [GDD](../GDD.md) · [TECH](../TECH.md) ·
[esquema de ficha](../WIKI.md#0-instrucciones-para-sistemas-de-ia)

## Cómo leer esta wiki

- Cada entidad es una **ficha YAML** con esquema fijo (WIKI §0). El campo `id`
  (snake_case) es el identificador canónico: se usa para nombres de archivo,
  clases, claves de datos y referencias cruzadas.
- `estado: canon` = decidido. `estado: propuesta` = pendiente de validar en
  prototipo.
- Los campos **`TBD`** están pendientes de balance y **no se inventan**
  (CLAUDE.md, regla 4). La columna *TBD* de las tablas cuenta cuántos tiene
  cada ficha.
- Regla de diseño de todo enemigo: **quiere llevarse algo** — qué roba, cómo
  lo roba, cómo se evita.
- De la wiki salen los datos del juego vía
  [`tools/wiki_to_resources.py`](../../tools/wiki_to_resources.py) → `data/`.
"""


def _row(cells: list[str]) -> str:
    return "| " + " | ".join(cells) + " |"


def _link(ficha: Ficha) -> str:
    return f"[`{ficha.id}`](../WIKI.md#{slug(ficha.block.section)})"


def _cell(value) -> str:
    """Un valor de ficha como celda de tabla (las listas se aplanan).

    Escapa `|`: hoy ninguna ficha lo usa, pero un solo pipe en un campo partiría
    la fila en dos columnas y el índice saldría corrupto en silencio.
    """
    if isinstance(value, list):
        return ", ".join(_cell(v) for v in value)
    if isinstance(value, dict):
        return ", ".join(f"{k}: {_cell(v)}" for k, v in value.items())
    return "" if value is None else str(value).replace("|", "\\|")


def _tbd_cell(ficha: Ficha) -> str:
    n = len(ficha.tbd_fields())
    return "—" if n == 0 else str(n)


def _estado_cell(ficha: Ficha) -> str:
    return "✅ canon" if ficha.estado == "canon" else f"🧪 {ficha.estado}"


def _table_section(
    title: str,
    wiki_heading: str,
    fichas: list[Ficha],
    columns: list[tuple[str, str]],
    intro: str = "",
) -> list[str]:
    """Una sección del índice: encabezado, enlace a la wiki y tabla de fichas.

    `columns` son los pares (encabezado, campo de la ficha) propios del tipo;
    las columnas Ficha / Estado / TBD son comunes a todas las tablas. Si no hay
    fichas de ese tipo, la sección no se emite (el índice no muestra tablas
    vacías).
    """
    if not fichas:
        return []
    out = [f"## {title}", ""]
    out.append(f"→ [Sección completa](../WIKI.md#{slug(wiki_heading)})")
    out.append("")
    if intro:
        out.append(intro)
        out.append("")
    out.append(_row(["Ficha"] + [h for h, _ in columns] + ["Estado", "TBD"]))
    out.append(_row(["---"] * (len(columns) + 3)))
    for f in fichas:
        out.append(
            _row(
                [_link(f)]
                + [_cell(f.data.get(field, "")) for _, field in columns]
                + [_estado_cell(f), _tbd_cell(f)]
            )
        )
    out.append("")
    return out


def build_index(fichas: list[Ficha]) -> str:
    units = [f for f in fichas if f.tipo == "unidad_jugador"]
    enemies = [f for f in fichas if f.tipo == "enemigo"]
    weapons = [f for f in fichas if f.tipo == "arma"]
    buildings = [f for f in fichas if f.tipo == "edificio"]
    waves = [f for f in fichas if f.tipo == "oleada"]
    resources = [f for f in fichas if f.tipo == "recurso"]

    out = [INDEX_PREAMBLE, "---", ""]

    out.append("## Unidades del jugador")
    out.append("")
    out.append(f"→ [Sección completa](../WIKI.md#{slug('1. Unidades del Jugador')})")
    out.append("")
    out.append(_row(["Ficha", "Nombre", "Rol", "Obtención", "Estado", "TBD"]))
    out.append(_row(["---"] * 6))
    for f in units:
        out.append(
            _row([
                _link(f),
                str(f.data.get("nombre", "")),
                str(f.data.get("rol", "")),
                str(f.data.get("obtencion", "")),
                _estado_cell(f),
                _tbd_cell(f),
            ])
        )
    out.append("")

    out.append("## Enemigos")
    out.append("")
    out.append(f"→ [Sección completa](../WIKI.md#{slug('2. Enemigos')})")
    out.append("")

    # Orden de categorías tal como aparecen en la wiki, sin reordenar.
    categories: list[str] = []
    for f in enemies:
        cat = str(f.data.get("categoria", "sin categoría"))
        if cat not in categories:
            categories.append(cat)

    for cat in categories:
        heading = next(
            (
                h
                for f in enemies
                if str(f.data.get("categoria")) == cat
                for lvl, h in f.block.headings.items()
                if lvl == 2 and "Categoría" in h
            ),
            "",
        )
        anchor = f"../WIKI.md#{slug(heading)}" if heading else "../WIKI.md#2-enemigos"
        out.append(f"### {cat.upper()}")
        out.append("")
        out.append(f"→ [Sección completa]({anchor})")
        out.append("")
        out.append(
            _row(["Ficha", "Nombre", "Qué roba", "Movimiento", "Aparición", "Estado", "TBD"])
        )
        out.append(_row(["---"] * 7))
        for f in [e for e in enemies if str(e.data.get("categoria")) == cat]:
            out.append(
                _row([
                    _link(f),
                    str(f.data.get("nombre", "")),
                    str(f.data.get("que_roba", "")),
                    str(f.data.get("movimiento", "")),
                    str(f.data.get("aparicion", "")),
                    _estado_cell(f),
                    _tbd_cell(f),
                ])
            )
        out.append("")

    out += _table_section(
        "Armas",
        "4. Armas",
        weapons,
        [("Nombre", "nombre"), ("Tier", "tier"), ("Montaje", "montaje"),
         ("Fabricación", "fabricacion")],
        intro="Solo las armas ya referenciadas por el `arma_base` de alguna unidad; "
        "el resto del árbol tecnológico sigue pendiente "
        "([GDD §8.1](../GDD.md#81-árbol-tecnológico-in-run)).",
    )

    out += _table_section(
        "Edificios",
        "5. Edificios",
        buildings,
        [("Nombre", "nombre"), ("Función", "funcion"), ("Slot", "slot"),
         ("Desbloquea", "desbloquea")],
    )

    out += _table_section(
        "Oleadas",
        "6. Oleadas",
        waves,
        [("Nombre", "nombre"), ("Noche", "noche"), ("Fase lunar", "fase_lunar"),
         ("Presupuesto", "presupuesto")],
        intro="La curva real de presupuesto por noche está pendiente "
        "([TECH §3.3](../TECH.md#33-wavedirector)).",
    )

    out += _table_section(
        "Recursos",
        "7. Recursos vivos y consumibles",
        resources,
        [("Nombre", "nombre"), ("Clase", "clase"), ("Fuente", "fuente"),
         ("Robable", "robable")],
        intro="La cadena del ganado (pasto → vaca → comida) y todo recurso con "
        "mecánica propia. Las materias primas sin mecánica (madera, chatarra) "
        "viven en [GDD §5.1](../GDD.md#51-recursos-sin-oro--decisión-tentativa).",
    )

    out.append("## Componentes (drops)")
    out.append("")
    out.append(
        f"La tabla canónica de componentes vive en "
        f"[WIKI §3](../WIKI.md#{slug('3. Registro de componentes (drops)')}). "
        f"Los componentes son la moneda del árbol tecnológico "
        f"([GDD §8](../GDD.md#81-árbol-tecnológico-in-run))."
    )
    out.append("")

    out.append("## Estado de completitud")
    out.append("")
    propuestas = [f for f in fichas if f.estado != "canon"]
    con_tbd = [f for f in fichas if f.tbd_fields()]
    desglose = ", ".join(
        f"{len(grupo)} {singular if len(grupo) == 1 else plural}"
        for singular, plural, grupo in (
            ("unidad", "unidades", units),
            ("enemigo", "enemigos", enemies),
            ("arma", "armas", weapons),
            ("edificio", "edificios", buildings),
            ("oleada", "oleadas", waves),
            ("recurso", "recursos", resources),
        )
        if grupo
    )
    out.append(f"- **{len(fichas)}** fichas ({desglose}).")
    out.append(
        f"- **{len(propuestas)}** en `estado: propuesta` — pendientes de validar: "
        + (", ".join(f"`{f.id}`" for f in propuestas) or "ninguna")
        + "."
    )
    out.append(
        f"- **{len(con_tbd)}** fichas con campos `TBD` pendientes de balance "
        f"({sum(len(f.tbd_fields()) for f in fichas)} campos en total)."
    )
    out.append("")
    return "\n".join(out)


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="Genera datos y navegación desde docs/WIKI.md (fuente canónica)."
    )
    ap.add_argument("--wiki", type=Path, default=WIKI_PATH, help="ruta a la wiki")
    ap.add_argument("--out", type=Path, default=DATA_DIR, help="carpeta de salida")
    ap.add_argument(
        "--format",
        choices=["json", "tres", "both"],
        default="json",
        help="json (por defecto) · tres (EXPERIMENTAL, ver TBD del escritor)",
    )
    ap.add_argument("--only", metavar="ID", help="generar solo esta ficha")
    ap.add_argument("--check", action="store_true", help="valida y reporta, no escribe")
    ap.add_argument(
        "--emit-index",
        action="store_true",
        help=f"regenera {WIKI_INDEX_PATH.relative_to(REPO_ROOT)}",
    )
    args = ap.parse_args(argv)

    try:
        fichas, warnings = load_fichas(args.wiki)
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    wiki_rel = str(args.wiki.resolve().relative_to(REPO_ROOT))
    print(f"wiki: {wiki_rel} — {len(fichas)} fichas")

    problems = [f"{f.id}: {p}" for f in fichas for p in f.problems()]
    for w in warnings:
        print(f"  aviso: {w}")
    for p in problems:
        print(f"  ERROR: {p}")

    tbd_total = sum(len(f.tbd_fields()) for f in fichas)
    propuestas = [f.id for f in fichas if f.estado != "canon"]
    print(f"  TBD pendientes de balance: {tbd_total} campos")
    print(f"  fichas en propuesta: {len(propuestas)} ({', '.join(propuestas) or '—'})")

    if args.emit_index:
        WIKI_INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)
        WIKI_INDEX_PATH.write_text(build_index(fichas), encoding="utf-8")
        print(f"  índice → {WIKI_INDEX_PATH.relative_to(REPO_ROOT)}")

    if args.check:
        return 1 if problems else 0

    targets = [f for f in fichas if not args.only or f.id == args.only]
    if args.only and not targets:
        print(f"error: no existe la ficha `{args.only}` en la wiki", file=sys.stderr)
        return 2

    written = 0
    for ficha in targets:
        out_dir = args.out / TIPO_TO_DIR[ficha.tipo]
        if args.format in ("json", "both"):
            write_json(ficha, out_dir, wiki_rel)
            written += 1
        if args.format in ("tres", "both"):
            write_tres(ficha, out_dir)
            written += 1
    if not args.only:
        write_manifest(targets, wiki_rel)
    print(f"  escritos: {written} archivos en {args.out.relative_to(REPO_ROOT)}/")
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
