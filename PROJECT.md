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

Desde el cambio de mecánica de v0.4 el robo es más concreto: **no hay muros.**
El rancho está abierto y de noche cada edificio se vuelve refugio o defensa. El
alien entra al refugio y **tarda** en sacar lo que hay (1–3 s por persona, 2 s
por recurso). No le impedís entrar: le cobrás esos segundos con torres que
colocás donde quieras. Y si lo matás cargado, suelta el botín.

## Documentos canónicos

| Documento | Ruta | Contenido |
|---|---|---|
| **GDD** | `docs/GDD.md` | Game Design Document v0.4 — visión, core loop, recursos, unidades, enemigos, **defensa sin muros** |
| **TECH** | `docs/TECH.md` | Documento técnico v0.1 — arquitectura, stack (Godot 4 + C#), plan de prototipo |
| **WIKI** | `docs/WIKI.md` | Wiki de entidades v0.2 — **fuente canónica** de unidades, enemigos, armas, edificios, oleadas, recursos, componentes (42 fichas YAML) |
| **Índice wiki** | `docs/wiki/README.md` | Navegación por categoría sobre la wiki (generado, no editar a mano) |

## Stack decidido

- **Motor:** Godot 4.x + C# (.NET)
- **Arte:** pixel art
- **Input:** gamepad primario, teclado soportado
- **Multijugador:** coop local 2 jugadores (split screen dinámico), sin online
- **Data-driven:** toda entidad se define en Resources generables desde la wiki

## Estado del desarrollo

- [x] GDD v0.4 (diseño) — completo; v0.4 aplica el cambio de mecánica de defensa
- [x] Documento técnico v0.1 (arquitectura) — *alineado en superficie con v0.4 (§2, §3.7, §4); falta el modelo técnico del refugio y del targeting (`TASK-019`)*
- [x] Wiki de entidades v0.2 (fuente canónica) — completa, con edificios día/noche y la cadena del ganado
- [x] Andamiaje de la wiki: índice navegable + pipeline wiki → datos
- [ ] Prototipo Godot (4-6 semanas, ver TECH §4)
- [ ] Vertical slice
- [ ] Loop completo
- [ ] Contenido (wiki completa implementada)

### Inventario de la wiki

42 fichas: **9 unidades** del jugador, **16 enemigos** (3 ladrones,
3 abductores, 3 tanques, 4 soporte, 3 jefes), **5 armas**, **9 edificios**,
**1 oleada** de ejemplo y **2 recursos** (`pasto`, `vaca`) + la tabla de
componentes.
26 fichas en `estado: propuesta` y 130 campos `TBD` pendientes de balance —
subieron con el cambio de mecánica: cinco enemigos que eran canon volvieron a
`propuesta` porque se diseñaron contra muros que ya no existen (`TASK-020`).
Conteo actualizado en cualquier momento con:

```bash
python3 tools/wiki_to_resources.py --check
```

Los esquemas de ficha están definidos — seis desde v0.2, con `recurso` (`TASK-003`
y el cambio de mecánica). Lo que falta es **contenido**, no forma: las armas del
árbol tecnológico T1/T2/T3 (§4 solo cubre las que alguna unidad ya referencia por
`arma_base`) y la curva real de oleadas (`TASK-008`).

### Cambio de mecánica v0.4 (agosto 2026)

Decidido por Mato: **el rancho no tiene muros.** La defensa son edificios que de
noche se vuelven refugio o defensa, más torres colocables y configurables por
prioridad de objetivo; el ganado come pasto y pasa hambre; los edificios suben
por una de dos ramas (refugio+defensa o doble refugio); y algunas entidades se
desbloquean cumpliendo objetivos (el científico llega con X vacas).

Quedan **seis decisiones abiertas** (D1–D6) que ningún agente resuelve por su
cuenta — están en [`docs/WIKI.md §9`](docs/WIKI.md), en GDD §13.1 y tienen dueño
en `TASK-018`, asignado a Mato. Se pueden cerrar de a una: solo las dos primeras
frenan trabajo; las otras cuatro viajan adentro del ticket que las necesita, con
la instrucción de parametrizar en vez de asumir.

| Decisión | Qué frena |
|---|---|
| **D1** — ¿los aliens atacan las torres o las ignoran? | **`TASK-013` está detenido.** La más urgente |
| **D2** — ¿entran los muros clásicos como opción? | **`TASK-020` está detenido** (los 5 enemigos que volvieron a `propuesta`) |
| **D3** — ¿cuánto tarda robarse una vaca? | nada: `TASK-014` usa un provisional marcado |
| **D4** — ¿cuántas vacas traen al científico? | nada: en `TASK-017` el umbral es un parámetro de data |
| **D5** — campo de fuerza, ¿estructura o arma T3? | nada: `TASK-016` es post-vertical-slice |
| **D6** — rama de nivel, ¿por edificio o global? | nada: `TASK-015` implementa por edificio tras una bandera |

## Cómo trabaja hivemind acá

Este repo es un proyecto **hivemind**: el orquestador planifica, los subagentes
(researcher, developer, reviewer) ejecutan, y el backlog vive en `tasks/`
(ver [`tasks/README.md`](tasks/README.md)). `CLAUDE.md` tiene el routing y las
reglas que no se negocian.

**Próximos pasos del backlog** — dos frentes en paralelo:

| Frente | Arranca por |
|---|---|
| **Decisiones (Mato)** | `TASK-018` (D1–D6) — D1 desbloquea `TASK-013`, D2 desbloquea `TASK-020` |
| Documentación | ~~`TASK-001`~~ ✅ → ~~`TASK-003`~~ ✅ → `TASK-019` (alinear TECH con v0.4) → `TASK-002` (cerrar GDD §13.2) |
| Juego | `TASK-006` (proyecto Godot, semana 1) → `TASK-007` (spike de split screen, riesgo #1) → `TASK-012` (edificios-refugio, el núcleo de v0.4) |
