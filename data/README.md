# `data/` — recursos generados

**Nada de esta carpeta se edita a mano.** Todo su contenido se genera desde
[`docs/WIKI.md`](../docs/WIKI.md) (la fuente canónica) con:

```bash
python3 tools/wiki_to_resources.py            # data/**/*.json + data/manifest.json
python3 tools/wiki_to_resources.py --check    # solo valida y reporta TBD
python3 tools/wiki_to_resources.py --format tres   # .tres de Godot (EXPERIMENTAL)
```

## Layout

| Carpeta | Contenido | Estado |
|---|---|---|
| `units/` | Una ficha por unidad del jugador (`peon`, `pistolero`, …) | generado |
| `enemies/` | Una ficha por enemigo, todas las categorías | generado |
| `weapons/` | Armas del árbol tecnológico | vacío — la wiki todavía no tiene esquema de arma |
| `buildings/` | Edificios del rancho | vacío — la wiki todavía no tiene esquema de edificio |
| `waves/` | Curvas de presupuesto por noche y modificador lunar | vacío — pendiente (TECH §3.3) |
| `manifest.json` | Índice de todas las entidades + campos `TBD` por ficha | generado |

## Por qué está en `.gitignore`

El contenido es derivado y reproducible desde la wiki, así que no se versiona
(solo este README). La contrapartida es que Godot necesita los `.tres`
presentes para abrir el proyecto — la decisión de versionarlos o generarlos en
un paso de build está abierta en el backlog (`tasks/`).

## Regla

Si un valor de balance está mal, **se corrige en la wiki**, no acá. Los campos
`TBD` se propagan tal cual: el pipeline nunca inventa balance.
