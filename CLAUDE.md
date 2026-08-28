# Western Defense — guía para agentes

Proyecto de videojuego (tower defense Weird West) gestionado con hivemind.
Este archivo define cómo trabajar en este repo.

## Identidad y fuentes

- **GDD:** `docs/GDD.md` — diseño, visión, mecánicas
- **TECH:** `docs/TECH.md` — arquitectura, stack, plan de implementación
- **WIKI:** `docs/WIKI.md` — **fuente canónica** de todas las entidades
  (unidades, enemigos, armas, edificios, oleadas, componentes). Fichas YAML con
  esquema fijo (cinco esquemas, definidos en §0).
- **Índice de la wiki:** `docs/wiki/README.md` — navegación por categoría.
  **Generado** desde la wiki; no lo edites a mano, regeneralo.

## Reglas que no se negocian

1. **La wiki es la fuente canónica.** Las fichas de `docs/WIKI.md` definen
   entidades; el código y los datos se generan desde ahí. No edites datos de
   entidades en código sin actualizar la wiki (o sincronizar de vuelta).
2. **La regla de diseño de todo enemigo:** *quiere llevarse algo*. Si generas
   enemigos nuevos, deben responder: ¿qué roba, cómo lo roba, cómo se evita?
3. **El robo duele más que la muerte.** Los enemigos roban (no destruyen); el
   fallo es una espiral, no un game over instantáneo.
4. **Nunca inventes valores de balance marcados `TBD`.** Los campos `TBD` en la
   wiki están pendientes de balance. Si se te pide proponer, marcá la ficha con
   `estado: propuesta` y justificá.
5. **Tono:** Weird West 1870s, cómic pulp — gracioso en la superficie,
   inquietante en la incertidumbre. Sin gore.
6. **Coop-ready siempre.** Ningún sistema asume "el jugador" en singular.

## Dónde está cada cosa

| Necesitás tocar | Andá a |
|---|---|
| Una unidad/enemigo/arma | `docs/WIKI.md` (ficha canónica) — buscala por `id` |
| Navegar la wiki | `docs/wiki/README.md` (índice generado) |
| El sitio público (GitHub Pages) | `docs/_config.yml`, `docs/_layouts/`, `docs/assets/`, `docs/index.md` y los envoltorios `docs/{diseno,tecnico,entidades}.md` |
| Arquitectura / stack / plan | `docs/TECH.md` |
| Reglas de diseño general | `docs/GDD.md` |
| Pipeline wiki → datos | `tools/wiki_to_resources.py` |
| Recursos de datos (generados) | `data/` (units/, enemies/, weapons/, buildings/, waves/) |
| Código C# | `src/` (Core/, Economy/, Units/, Enemies/, Buildings/, Tech/, Coop/, UI/) |
| Escenas Godot | `scenes/` |
| Arte | `art/` |

## Comandos

```bash
# Pipeline wiki → datos (sin dependencias externas, Python 3 pelado)
python3 tools/wiki_to_resources.py --check        # valida fichas, cuenta TBD, no escribe
python3 tools/wiki_to_resources.py                # genera data/**/*.json + manifest
python3 tools/wiki_to_resources.py --only peon    # una sola ficha
python3 tools/wiki_to_resources.py --format tres  # .tres de Godot (ANDAMIO, ver TASK-004)
python3 tools/wiki_to_resources.py --emit-index   # regenera docs/wiki/README.md
```

**Después de tocar `docs/WIKI.md`, corré `--emit-index`** o el índice queda
desincronizado de la fuente canónica.

## Sitio público

La documentación se publica en <https://lordiwa.github.io/western-defense/>
(GitHub Pages, Jekyll nativo desde `main` + `/docs`; cada push la reconstruye).

- **Los documentos canónicos no llevan nada del sitio.** `GDD.md`, `TECH.md`,
  `WIKI.md` y `wiki/README.md` siguen siendo markdown limpio, sin front matter.
  Las páginas `docs/diseno.md`, `docs/tecnico.md` y `docs/entidades.md` los
  incluyen con `{% include_relative %}`. Así el equipo puede seguir reemplazando
  los canónicos enteros sin romper el sitio.
- **No metas `{{` ni `{%` en los documentos canónicos**: Jekyll los interpreta
  como Liquid al incluirlos y el build falla. Si hace falta, escapalos.
- Los enlaces `.md` y las anclas estilo GitHub (con acentos y números de
  sección) los arregla `docs/assets/js/wiki.js` en el navegador — no hay que
  reescribir enlaces en el markdown canónico.
- Si agregás una sección al sitio, sumala a `nav:` en `docs/_config.yml`.

```bash
# (comandos de Godot: a completar en TASK-006)
```

## Convenciones

- **Fichas YAML** en la wiki con el esquema definido en `docs/WIKI.md §0`.
- `id` es el identificador canónico (snake_case, estable) — para nombres de
  archivo, clases, claves de datos y referencias cruzadas.
- **Commits:** Conventional Commits.
- El pipeline `wiki → data` se diseñó para que un agente proponga cambios de
  balance como PRs sobre la wiki (ver TECH §3.7).

## Estado

Backlog y decisiones en `tasks/` (formato en `tasks/README.md`) y `state/`.
Ver `PROJECT.md` para el estado del desarrollo.

Los tres documentos canónicos están **completos** desde `TASK-001` (los
originales llegaron del equipo y reemplazaron las colas truncadas del commit
inicial): GDD §13 + Anexo A + Roadmap, y la tabla de componentes de WIKI §3.
`python3 tools/wiki_to_resources.py --check` verifica que sigan completos.
