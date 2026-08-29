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
alien entra al refugio y **tarda** en sacar lo que hay (**3–5 s por cosa**, sea
aldeano, comida o vaca; los grandes se llevan dos y tardan más — D3). No le impedís entrar: le cobrás esos segundos con torres que
colocás donde quieras. Y si lo matás cargado, suelta el botín.

## Documentos canónicos

| Documento | Ruta | Contenido |
|---|---|---|
| **GDD** | `docs/GDD.md` | Game Design Document v0.4 — visión, core loop, recursos, unidades, enemigos, **defensa sin muros** |
| **TECH** | `docs/TECH.md` | Documento técnico v0.1 — arquitectura, stack (Godot 4 + C#), plan de prototipo |
| **WIKI** | `docs/WIKI.md` | Wiki de entidades v0.2 — **fuente canónica** de unidades, enemigos, armas, edificios, oleadas, recursos, **clases de héroe**, componentes (46 fichas YAML) |
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

46 fichas: **9 unidades** del jugador, **16 enemigos** (3 ladrones,
3 abductores, 3 tanques, 4 soporte, 3 jefes), **5 armas**, **9 edificios**,
**1 oleada** de ejemplo, **3 recursos** (`pasto`, `vaca`, `pieza_alien`) y
**3 clases de héroe** (`hero_clase_sheriff`, `hero_clase_alcalde`,
`hero_clase_carpintero`) + la tabla de componentes.
28 fichas en `estado: propuesta` y 139 campos `TBD` pendientes de balance —
subieron con el cambio de mecánica: cinco enemigos que eran canon volvieron a
`propuesta` porque se diseñaron contra muros que ya no existen (`TASK-020`).
Conteo actualizado en cualquier momento con:

```bash
python3 tools/wiki_to_resources.py --check
```

Los esquemas de ficha están definidos — siete: los seis de v0.2 con `recurso`
(`TASK-003` y el cambio de mecánica) más `clase_heroe` (las clases del héroe). Lo que falta es **contenido**, no forma: las armas del
árbol tecnológico T1/T2/T3 (§4 solo cubre las que alguna unidad ya referencia por
`arma_base`) y la curva real de oleadas (`TASK-008`).

### Cambio de mecánica v0.4 (agosto 2026)

Decidido por Mato: **el rancho no tiene muros.** La defensa son edificios que de
noche se vuelven refugio o defensa, más torres colocables y configurables por
prioridad de objetivo; el ganado come pasto y pasa hambre; los edificios suben
por una de dos ramas (refugio+defensa o doble refugio); y algunas entidades se
desbloquean cumpliendo objetivos (el científico llega con X vacas).

Las **seis decisiones** que dejó ese cambio (D1–D6) están **cerradas**: Mato
respondió cinco el 29 de agosto de 2026 y la sexta (D4) pasó a ser una fase de
balance. `TASK-018` está `done`. El registro canónico es
[`docs/WIKI.md §9`](docs/WIKI.md), con resumen en GDD §13.1.

| Decisión | Qué se decidió | Qué destrabó |
|---|---|---|
| **D1** ✅ | Variante A: los aliens **atacan las torres primero** y resuelven la que los engancha antes de ir al refugio | **`TASK-013` destrabado** (`todo`) |
| **D2** ✅ | **Sin muros**, ni siquiera como variante: rancho abierto, `barricada` archivada | **`TASK-020` destrabado** (`todo`) — los 5 enemigos en `propuesta` |
| **D3** ✅ | **3–5 s por cosa robada**, igual para aldeano, comida y vaca; los grandes se llevan dos | `TASK-014` deja de usar provisional |
| **D4** ⏳ | **No es decisión, es balance**: la curva de checkpoints la propone `TASK-021` y la aprueba Mato. **Propuesta escrita** (cuatro compuertas, WIKI §8.1) — **espera a Mato** | El umbral sigue `TBD` como parámetro de data en `TASK-017` |
| **D5** ✅ | El campo de fuerza es **estructura** y desbloqueo post-científico, pagado en `pieza_alien` (barrido del amanecer) | `TASK-016` sigue post-vertical-slice |
| **D6** ✅ | **Árbol de talentos por edificio**, sin árbol global | `TASK-015` implementa por edificio, sin bandera |

### Clases del héroe (29 de agosto de 2026)

Decidido por Mato: **el héroe del jugador tiene clase**, y son tres —
**Sheriff** (sube el ataque de tus edificios y unidades), **Alcalde** (sube la
economía y la producción de recursos) y **Carpintero** (sube la defensa de tus
recursos y la capacidad de tus edificios). Una clase = un eje; se elige al
empezar la run y en coop cada héroe lleva la suya sobre el mismo rancho.

Las tres clases son además el **marco de la meta-progresión roguelite**
(GDD §8.3): los puntos de fin de run se gastan en **mejorar tu héroe** o
**desbloquear héroes nuevos** que pertenecen a una de esas tres clases.

Fichas canónicas en [`docs/WIKI.md §11`](docs/WIKI.md) (séptimo esquema,
`clase_heroe`), resumen en GDD §4.3 y §8.3, tickets `TASK-023` (sistema en run)
y `TASK-024` (meta entre runs). **Las magnitudes de los bonus son `TBD`**: no se
inventan, salen de la pasada de balance y las aprueba Mato.

## Cómo trabaja hivemind acá

Este repo es un proyecto **hivemind**: el orquestador planifica, los subagentes
(researcher, developer, reviewer) ejecutan, y el backlog vive en `tasks/`
(ver [`tasks/README.md`](tasks/README.md)). `CLAUDE.md` tiene el routing y las
reglas que no se negocian.

**Próximos pasos del backlog** — dos frentes en paralelo:

| Frente | Arranca por |
|---|---|
| **Decisiones (Mato)** | ~~`TASK-018`~~ ✅ (D1–D6 cerradas) → `TASK-021` (curva de progresión de D4, la aprueba Mato) |
| Documentación | ~~`TASK-001`~~ ✅ → ~~`TASK-003`~~ ✅ → `TASK-019` (alinear TECH con v0.4) → `TASK-002` (cerrar GDD §13.2) |
| Juego | `TASK-006` (proyecto Godot, semana 1) → `TASK-007` (spike de split screen, riesgo #1) → `TASK-012` (edificios-refugio, el núcleo de v0.4) → `TASK-023` (clases del héroe) |
| Meta-juego | `TASK-023` (las tres clases en la run) → `TASK-024` (roguelite de héroes entre runs) |
