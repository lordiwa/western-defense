# COWBOY DEFENSE — Documento Técnico v0.1

> **Propósito:** Arquitectura, stack y plan de implementación. Acompaña a [`GDD.md`](GDD.md) y [`WIKI.md`](WIKI.md) ([índice](wiki/README.md)).
> **Stack decidido:** Godot 4.x + C# (.NET). Ver GDD Anexo A para la justificación vs Unity/Phaser.

---

## 1. Principios técnicos

1. **Data-driven desde el día uno.** Toda entidad (unidad, enemigo, arma, edificio) se define en Resources (`.tres`) generables desde las fichas de la wiki. El código implementa comportamientos; los datos viven fuera. Esto habilita que sistemas agénicos generen/balanceen contenido sin tocar código.
2. **Coop-ready siempre.** Ningún sistema asume "el jugador" en singular: cámara, input, HUD y órdenes operan sobre `List<Hero>` (1–2). Parchear coop después es el riesgo técnico #1 del proyecto.
3. **Simulación desacoplada del render.** La lógica de oleadas, robo y economía corre en managers puros testeables; los nodos de Godot solo presentan.
4. **Determinismo razonable.** Seed por run para la generación del mapa/fondo y composición de oleadas → reproducibilidad de bugs y balance.

---

## 2. Estructura del proyecto

```
cowboy-defense/
├── project.godot
├── src/                        # C#
│   ├── Core/
│   │   ├── GameManager.cs          # estado del run, ciclo día/noche
│   │   ├── TimeCycle.cs            # reloj, fases, ciclo lunar
│   │   ├── RunSeed.cs              # RNG con seed
│   │   └── SaveSystem.cs           # meta-progresión (JSON en user://)
│   ├── Economy/
│   │   ├── ResourceLedger.cs       # madera, chatarra, comida, población
│   │   ├── ResourcePickup.cs       # recursos físicos en el mundo
│   │   └── FoodUpkeep.cs           # consumo diario, deserción/hambre
│   ├── Units/
│   │   ├── UnitBase.cs             # FSM base + stats desde Resource
│   │   ├── UnitAI/                 # estados: Recolectar, Construir, Defender, Refugiarse, Reparar
│   │   ├── HeroController.cs       # input, disparo automático, estados de derribo
│   │   └── AbductableComponent.cs  # TODO lo raptable lo lleva (unidades, ganado, recursos)
│   ├── Enemies/
│   │   ├── EnemyBase.cs            # FSM base por categoría
│   │   ├── Behaviors/              # Ladron, Abductor, Tanque, Soporte, Jefe
│   │   ├── TheftSystem.cs          # qué carga cada enemigo, drop al morir, huida al amanecer
│   │   └── WaveDirector.cs         # presupuesto por noche × modificador lunar → composición
│   ├── Buildings/
│   │   ├── BuildingBase.cs         # slots, niveles, HP
│   │   ├── BuildSlotManager.cs     # layout fijo del rancho
│   │   └── RepairSystem.cs         # reparación bajo fuego
│   ├── Tech/
│   │   ├── TechTree.cs             # recetas, requisitos de componentes
│   │   └── ComponentInventory.cs   # drops recogidos (wiki §3)
│   ├── Coop/
│   │   ├── PlayerInputRouter.cs    # device → héroe
│   │   └── DynamicSplitScreen.cs   # SubViewports; merge/split por distancia
│   └── UI/
├── data/                       # Resources generados desde la wiki
│   ├── units/      (peon.tres, pistolero.tres, ...)
│   ├── enemies/    (ratero_gris.tres, ...)
│   ├── weapons/
│   ├── buildings/
│   └── waves/      (curvas de presupuesto por noche)
├── scenes/
│   ├── Main.tscn
│   ├── World.tscn              # terreno + capas parallax generadas
│   ├── units/, enemies/, buildings/
│   └── ui/
├── art/                        # sprites, paletas
└── tools/
    └── wiki_to_resources.py    # parsea WIKI_*.md → .tres (pipeline agéntico)
```

---

## 3. Sistemas clave — notas de diseño técnico

### 3.1 TimeCycle (día/noche/luna)
- Reloj único que emite señales: `DayStarted`, `DuskWarning`, `NightStarted`, `DawnStarted`.
- Fase lunar como índice del ciclo (config en `data/waves/`); `IsFullMoon` modifica el presupuesto del WaveDirector y activa spawns exclusivos (`faro_lunar`, `nave_capataz`).
- Duraciones fijas por fase, configurables por dificultad.

### 3.2 TheftSystem (el corazón del juego)
- `AbductableComponent` en todo lo robable: unidades, ganado, pickups de recursos.
- Un enemigo con carga referencia a su víctima; **si muere antes de salir de pantalla → la víctima se libera viva** (la vaca cae, el aldeano se suelta).
- Al `DawnStarted`, todo enemigo entra en estado `Flee`; lo que saque de los límites del mundo se destruye permanentemente y se registra en el resumen del día.
- Resumen post-noche: qué se perdió, qué se salvó, qué componentes cayeron — pantalla clave para que "el robo duela" de forma legible.

### 3.3 WaveDirector
- Presupuesto de puntos por noche (curva en data) × modificador lunar.
- Cada enemigo tiene costo en puntos + restricciones de aparición (`aparicion` de la wiki).
- Composición determinista por seed; spawn por flancos izquierda/derecha, voladores con paths propios.

### 3.4 HeroController — estados de derribo
- FSM: `Normal → Derribado (stun) → Malherido (multiplicadores de velocidad/cadencia) → FueraDeCombate`.
- `FueraDeCombate`: se desactiva el control del héroe, el input del jugador pasa a un `SpectatorCamera` libre; el cuerpo queda donde cayó; al `DawnStarted` revive en ese punto en estado `Malherido`.
- Cada héroe del coop lleva su propia FSM.

### 3.5 DynamicSplitScreen (coop)
- Dos `SubViewport` + `Camera2D` por héroe.
- Si `distancia(h1, h2) < umbral` → una sola cámara (viewport unificado con lerp del punto medio); si se separan → transición a split vertical.
- En 1 jugador el sistema colapsa a cámara única — mismo código, cero rama especial.
- Riesgo de rendimiento bajo en 2D pixel art; validar en semana 1 igualmente (es la pieza con más incertidumbre de UX).

### 3.6 Generación del mundo por run
- Layout jugable fijo (posiciones de town center, slots, flancos, nodriza).
- Con el seed: distribución de árboles, sitios de chatarra, puntos de caza y reclutas dentro de zonas predefinidas; composición de capas parallax del fondo desde un pool de piezas.
- El "arte generativo" del fondo entra al pipeline de assets (herramientas de generación → curación humana → pool de piezas), no a runtime.

### 3.7 Pipeline wiki → datos
- `tools/wiki_to_resources.py` parsea los bloques YAML de [`docs/WIKI.md`](WIKI.md) y genera/actualiza los recursos en `data/`. Hoy es un **andamio**: emite JSON completo para las 25 fichas + `data/manifest.json`, valida campos requeridos y contabiliza los `TBD` sin rellenarlos; el escritor `.tres` (`--format tres`) es un esqueleto a la espera de las clases Resource de C# de §2. El mismo script regenera el índice navegable de la wiki con `--emit-index`.
- Regla: **la wiki es la fuente canónica**; el balance se edita en la wiki (o en los .tres y se sincroniza de vuelta). Diseñado para que un agente proponga cambios de balance como PRs sobre la wiki.

---

## 4. Plan de implementación — Prototipo (4–6 semanas)

**Meta del prototipo:** validar que "el robo duele" se siente, con arte placeholder.

| Semana | Entregable |
|---|---|
| 1 | Proyecto Godot + C#; TimeCycle; héroe con movimiento y disparo automático; spike de DynamicSplitScreen (validar riesgo) |
| 2 | ResourceLedger + pickups físicos; Peón con FSM (recolectar/depositar); barricada construible |
| 3 | `ratero_gris` completo (entra, roba, huye) + TheftSystem; WaveDirector mínimo; primera noche jugable |
| 4 | `platillo_sonda` + ganado + rayo tractor + rescate por derribo (la vaca cae viva) |
| 5 | Reparación bajo fuego; estados de derribo del héroe; resumen post-noche; espiral de derrota funcional |
| 6 | Buffer: balance de 5 noches jugables, playtest a 2 jugadores, decisión go/no-go sobre sensaciones del core |

**Criterio de éxito del prototipo:** un playtester describe espontáneamente la experiencia en términos de lo que le *robaron*, no de lo que *destruyeron*.

## 5. Fases posteriores (resumen)
1. **Vertical slice:** economía completa (comida/hambre), 5–6 enemigos, árbol tec T1→T2, primera luna llena, coop pulido.
2. **Loop completo:** asalto a la nodriza, meta-progresión, save system.
3. **Contenido:** wiki completa implementada, T3, jefes, generación de fondo por pool.

## 6. Riesgos técnicos
| Riesgo | Mitigación |
|---|---|
| Split screen dinámico se siente mal | Spike en semana 1; plan B: split fijo al separarse |
| IA de unidades frustrante (síndrome Kingdom: aldeanos suicidas) | FSMs simples + reglas de refugio agresivas; playtests tempranos enfocados en esto |
| Rampa Godot para el equipo (viene de Unity) | C# minimiza el salto; primera semana es intencionalmente infraestructura simple |
| Consolas en Godot | Diferido; W4 Games u otro porting partner cuando haya tracción en Steam |
| Balance de la espiral de robo (o muy punitiva o irrelevante) | Todo en data + seed determinista → iteración rápida; telemetría simple de runs desde el prototipo |

---

*Documento técnico v0.1 — se actualiza tras el spike de semana 1 y el cierre del prototipo.*