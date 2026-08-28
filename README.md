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
| [`docs/GDD.md`](docs/GDD.md) | Game Design Document v0.3 |
| [`docs/TECH.md`](docs/TECH.md) | Documento técnico v0.1 |
| [`docs/WIKI.md`](docs/WIKI.md) | Wiki de entidades v0.1 (fuente canónica) |

## Stack

- **Motor:** Godot 4.x + C# (.NET)
- **Arte:** pixel art
- **Coop:** local 2 jugadores (split screen dinámico), sin online

## Estado

Pre-producción: documentación y diseño completos. El prototipo Godot (4-6
semanas) es el siguiente hito — ver [docs/TECH.md](docs/TECH.md) §4.

## Desarrollo

Proyecto gestionado con hivemind: el orquestador planifica, los subagentes
ejecutan, el backlog vive en `tasks/`. Ver `CLAUDE.md`.
