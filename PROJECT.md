# WESTERN DEFENSE — Project Identity

> **Nombre tentativo:** Cowboy Defense (working title)
> **Nombre del repo:** western-defense
> **Equipo:** 2 personas + sistemas agénicos (hivemind)
> **Estado:** Pre-producción — documentación y diseño

## ¿Qué es esto?

Un **tower defense de scroll lateral 2D** ambientado en el Viejo Oeste (1870s,
Weird West). De día exploras el desierto y gestionas tu rancho con control
indirecto; de noche, alienígenas atacan para **robarte** — gente, ganado,
recursos. Cada cosa que te roban te debilita para el día siguiente. Recuperas
tecnología alienígena de los enemigos caídos para mejorar tus armas y torres,
hasta poder marchar contra la nave nodriza y liberar el valle.

## El hook diferenciador

Los enemigos **no destruyen: roban.** El fallo no es binario (game over
instantáneo) sino una espiral: cada noche mala te quita brazos, comida y
defensas para la siguiente. Y el arco de poder es irónico: terminas
defendiéndote de los aliens **con sus propias armas**.

## Documentos canónicos

| Documento | Ruta | Contenido |
|---|---|---|
| **GDD** | `docs/GDD.md` | Game Design Document v0.3 — visión, core loop, recursos, unidades, enemigos |
| **TECH** | `docs/TECH.md` | Documento técnico v0.1 — arquitectura, stack (Godot 4 + C#), plan de prototipo |
| **WIKI** | `docs/WIKI.md` | Wiki de entidades v0.1 — **fuente canónica** de unidades, enemigos, componentes (fichas YAML) |

## Stack decidido

- **Motor:** Godot 4.x + C# (.NET)
- **Arte:** pixel art
- **Input:** gamepad primario, teclado soportado
- **Multijugador:** coop local 2 jugadores (split screen dinámico), sin online
- **Data-driven:** toda entidad se define en Resources generables desde la wiki

## Estado del desarrollo

- [x] GDD v0.3 (diseño)
- [x] Documento técnico v0.1 (arquitectura)
- [x] Wiki de entidades v0.1 (fuente canónica)
- [ ] Prototipo Godot (4-6 semanas, ver TECH §4)
- [ ] Vertical slice
- [ ] Loop completo
- [ ] Contenido (wiki completa implementada)

## Cómo trabaja hivemind acá

Este repo es un proyecto **hivemind**: el orquestador planifica, los subagentes
(researcher, developer, reviewer) ejecutan, y el backlog vive en `tasks/`.
Ver `CLAUDE.md` para el routing y las reglas.
