# Western Defense

Tower defense de scroll lateral 2D ambientado en el Viejo Oeste (1870s, Weird
West). De día exploras el desierto y gestionas tu rancho con control indirecto;
de noche, alienígenas atacan para **robarte** — gente, ganado, recursos.
Recuperas tecnología alienígena de los enemigos caídos para mejorar tus armas y
torres, hasta poder marchar contra la nave nodriza y liberar el valle.

**Los enemigos no destruyen: roban.** El fallo es una espiral, no un game over.

## Documentación

| Documento | Descripción |
|---|---|
| [`docs/GDD.md`](docs/GDD.md) | Game Design Document v0.3 — visión, core loop, recursos |
| [`docs/TECH.md`](docs/TECH.md) | Documento técnico v0.1 — arquitectura, stack, plan |
| [`docs/WIKI.md`](docs/WIKI.md) | Wiki de entidades v0.1 — **fuente canónica** (25 fichas YAML) |
| [`docs/wiki/README.md`](docs/wiki/README.md) | **Índice navegable de la wiki** — tablas por categoría (generado) |

## Pipeline wiki → datos

Las entidades del juego se definen una sola vez, en la wiki, y de ahí se
generan los datos y la navegación:

```bash
python3 tools/wiki_to_resources.py --check        # valida fichas, reporta TBD
python3 tools/wiki_to_resources.py                # genera data/**/*.json
python3 tools/wiki_to_resources.py --emit-index   # regenera docs/wiki/README.md
```

Sin dependencias externas. `data/` es contenido derivado y no se versiona —
ver [`data/README.md`](data/README.md).

## Stack

- **Motor:** Godot 4.x + C# (.NET)
- **Arte:** pixel art
- **Coop:** local 2 jugadores (split screen dinámico), sin online

## Estado

Pre-producción. El prototipo Godot (4-6 semanas) es el siguiente hito — ver
[docs/TECH.md](docs/TECH.md) §4.

> ⚠️ `docs/GDD.md` y `docs/WIKI.md` están **truncados** al final desde el
> commit inicial: falta la §13 del GDD (Preguntas Abiertas) y la última fila de
> la tabla de componentes de la wiki. Restaurarlas es `TASK-001`, el primer
> bloqueante del backlog.

## Desarrollo

Proyecto gestionado con hivemind: el orquestador planifica, los subagentes
ejecutan, el backlog vive en [`tasks/`](tasks/README.md). Ver `CLAUDE.md` para
el routing y las reglas que no se negocian.
