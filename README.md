# Western Defense

Tower defense de scroll lateral 2D ambientado en el Viejo Oeste (1870s, Weird
West). De día exploras el desierto y gestionas tu rancho con control indirecto;
de noche, alienígenas atacan para **robarte** — gente, ganado, recursos.
Recuperas tecnología alienígena de los enemigos caídos para mejorar tus armas y
torres, hasta poder marchar contra la nave nodriza y liberar el valle.

**Los enemigos no destruyen: roban.** El fallo es una espiral, no un game over.

Y roban **de adentro de tus edificios**: no hay muros. El rancho está abierto,
de noche cada edificio se vuelve refugio o defensa, y al alien le lleva tiempo
sacar lo que hay (1–3 s por persona, 2 s por recurso). No le impedís entrar —
le cobrás esos segundos con torres que colocás donde quieras.

## Documentación

📖 **Se lee en el navegador: <https://lordiwa.github.io/western-defense/>**
(GitHub Pages, publicado desde `docs/` en `main` — se actualiza solo con cada push).

| Documento | En el sitio | Descripción |
|---|---|---|
| [`docs/GDD.md`](docs/GDD.md) | [/GDD.html](https://lordiwa.github.io/western-defense/GDD.html) | Game Design Document v0.4 — visión, core loop, recursos, defensa sin muros |
| [`docs/TECH.md`](docs/TECH.md) | [/TECH.html](https://lordiwa.github.io/western-defense/TECH.html) | Documento técnico v0.1 — arquitectura, stack, plan |
| [`docs/WIKI.md`](docs/WIKI.md) | [/WIKI.html](https://lordiwa.github.io/western-defense/WIKI.html) | Wiki de entidades v0.2 — **fuente canónica** (42 fichas YAML) |
| [`docs/wiki/README.md`](docs/wiki/README.md) | [/wiki/](https://lordiwa.github.io/western-defense/wiki/) | **Índice navegable de la wiki** — tablas por categoría (generado) |

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

Los tres documentos canónicos están completos desde `TASK-001`.
`python3 tools/wiki_to_resources.py --check` verifica que sigan estándolo.

## Desarrollo

Proyecto gestionado con hivemind: el orquestador planifica, los subagentes
ejecutan, el backlog vive en [`tasks/`](tasks/README.md). Ver `CLAUDE.md` para
el routing y las reglas que no se negocian.
