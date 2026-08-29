# Western Defense — guía para agentes

Proyecto de videojuego (tower defense Weird West) gestionado con hivemind.
Este archivo define cómo trabajar en este repo.

## Identidad y fuentes

- **GDD:** `docs/GDD.md` — diseño, visión, mecánicas
- **TECH:** `docs/TECH.md` — arquitectura, stack, plan de implementación
- **WIKI:** `docs/WIKI.md` — **fuente canónica** de todas las entidades
  (unidades, enemigos, armas, edificios, oleadas, recursos, clases de héroe,
  componentes). Fichas YAML con esquema fijo (siete esquemas, definidos en §0 —
  el sexto es `recurso` y el séptimo `clase_heroe`, las tres clases del héroe
  de §11).
- **Índice de la wiki:** `docs/wiki/README.md` — navegación por categoría.
  **Generado** desde la wiki; no lo edites a mano, regeneralo.

## Reglas que no se negocian

1. **La wiki es la fuente canónica.** Las fichas de `docs/WIKI.md` definen
   entidades; el código y los datos se generan desde ahí. No edites datos de
   entidades en código sin actualizar la wiki (o sincronizar de vuelta).
2. **La regla de diseño de todo enemigo:** *quiere llevarse algo*. Si generas
   enemigos nuevos, deben responder: ¿qué roba, cómo lo roba, cómo se evita?
3. **El robo duele más que la muerte.** Los enemigos roban (no destruyen); el
   fallo es una espiral, no un game over instantáneo. Desde v0.4 roban **a los
   edificios**: no hay muros, cada edificio es refugio o defensa de noche, y
   sacar cada víctima les lleva tiempo (**3–5 s por cosa** — aldeano, comida o
   vaca, el mismo rango para las tres; los aliens grandes se llevan dos y tardan
   más, D3).
   Esa ventana es toda la defensa del juego. Ver WIKI §5.0 (normativo).
4. **Las decisiones abiertas son de Mato.** WIKI §9 (D1–D6) y GDD §13.1 listan
   preguntas que ningún agente contesta por su cuenta, ni por deducción ni por
   default silencioso. Tienen dueño en `TASK-018`, asignado a Mato. Si una te
   bloquea: parametrizá y dejá el valor marcado como provisional, y seguí con
   lo que no dependa de ella.
5. **Nunca inventes valores de balance marcados `TBD`.** Los campos `TBD` en la
   wiki están pendientes de balance. Si se te pide proponer, marcá la ficha con
   `estado: propuesta` y justificá.
6. **Tono:** Weird West 1870s, cómic pulp — gracioso en la superficie,
   inquietante en la incertidumbre. Sin gore.
7. **Coop-ready siempre.** Ningún sistema asume "el jugador" en singular.

## Dónde está cada cosa

| Necesitás tocar | Andá a |
|---|---|
| Una unidad/enemigo/arma | `docs/WIKI.md` (ficha canónica) — buscala por `id` |
| Navegar la wiki | `docs/wiki/README.md` (índice generado) |
| El sitio público (GitHub Pages) | `docs/_config.yml`, `docs/_layouts/`, `docs/assets/`, `docs/index.md` |
| Arquitectura / stack / plan | `docs/TECH.md` |
| Reglas de diseño general | `docs/GDD.md` |
| Pipeline wiki → datos | `tools/wiki_to_resources.py` |
| Recursos de datos (generados) | `data/` (units/, enemies/, weapons/, buildings/, waves/, resources/, hero_classes/) |
| Las tres clases del héroe | `docs/WIKI.md §11` + GDD §4.3 y §8.3 |
| Las decisiones abiertas de Mato | `docs/WIKI.md §9` (D1–D6) + GDD §13.1 + `tasks/TASK-018.json` |
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

| Página | Archivo que la genera |
|---|---|
| `/` | `docs/index.md` (portada, escrita para el sitio) |
| `/GDD.html` | `docs/GDD.md` — **canónico, sin tocar** |
| `/TECH.html` | `docs/TECH.md` — **canónico, sin tocar** |
| `/WIKI.html` | `docs/WIKI.md` — **canónico, sin tocar** |
| `/wiki/` | `docs/wiki/README.md` — índice generado |

- **Los documentos canónicos no llevan NADA del sitio**: ni front matter ni
  marcadores de Jekyll. Se publican gracias a plugins que GitHub Pages trae
  activados (`jekyll-optional-front-matter`, `jekyll-readme-index`,
  `jekyll-relative-links`). El único andamiaje es `docs/_config.yml`, que les
  aplica el layout con `defaults`. El equipo puede seguir reemplazando los
  canónicos enteros y el sitio no se entera.
- **Los enlaces `.md` entre documentos se resuelven solos** (jekyll-relative-links)
  y las anclas coinciden con las de GitHub. No hay que reescribir nada.
- **No metas `{{` ni `{%` en los documentos canónicos**: Jekyll los interpreta
  como Liquid y el build falla. Si hace falta, escapalos.
- `docs/assets/js/wiki.js` es solo comodidad (índice de contenidos, tablas con
  scroll, volver arriba). Sin JS el sitio se lee igual.
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
