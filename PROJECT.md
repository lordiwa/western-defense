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
| **WIKI** | `docs/WIKI.md` | Wiki de entidades v0.1 — **fuente canónica** de unidades, enemigos, armas, edificios, oleadas, componentes (39 fichas YAML) |
| **Índice wiki** | `docs/wiki/README.md` | Navegación por categoría sobre la wiki (generado, no editar a mano) |

## Stack decidido

- **Motor:** Godot 4.x + C# (.NET)
- **Arte:** pixel art
- **Input:** gamepad primario, teclado soportado
- **Multijugador:** coop local 2 jugadores (split screen dinámico), sin online
- **Data-driven:** toda entidad se define en Resources generables desde la wiki

## Estado del desarrollo

- [x] GDD v0.3 (diseño) — completo (§13, Anexo A y Roadmap restaurados en `TASK-001`)
- [x] Documento técnico v0.1 (arquitectura)
- [x] Wiki de entidades v0.1 (fuente canónica) — completa (§3 cerrada en `TASK-001`)
- [x] Andamiaje de la wiki: índice navegable + pipeline wiki → datos
- [ ] Prototipo Godot (4-6 semanas, ver TECH §4)
- [ ] Vertical slice
- [ ] Loop completo
- [ ] Contenido (wiki completa implementada)

### Inventario de la wiki

39 fichas: **9 unidades** del jugador, **16 enemigos** (3 ladrones,
3 abductores, 3 tanques, 4 soporte, 3 jefes), **5 armas**, **8 edificios** y
**1 oleada** de ejemplo + la tabla de componentes.
19 fichas en `estado: propuesta` y 110 campos `TBD` pendientes de balance —
conteo actualizado en cualquier momento con:

```bash
python3 tools/wiki_to_resources.py --check
```

Los cinco esquemas de ficha están definidos (`TASK-003`). Lo que falta es
**contenido**, no forma: las armas del árbol tecnológico T1/T2/T3 (§4 solo cubre
las que alguna unidad ya referencia por `arma_base`) y la curva real de oleadas
(`TASK-008`).

## Cómo trabaja hivemind acá

Este repo es un proyecto **hivemind**: el orquestador planifica, los subagentes
(researcher, developer, reviewer) ejecutan, y el backlog vive en `tasks/`
(ver [`tasks/README.md`](tasks/README.md)). `CLAUDE.md` tiene el routing y las
reglas que no se negocian.

**Próximos pasos del backlog** — dos frentes en paralelo:

| Frente | Arranca por |
|---|---|
| Documentación | ~~`TASK-001`~~ ✅ → `TASK-003` (esquemas de arma/edificio/oleada) → `TASK-002` (cerrar GDD §13, necesita decisiones del equipo) |
| Juego | `TASK-006` (proyecto Godot, semana 1) → `TASK-007` (spike de split screen, riesgo #1) |
