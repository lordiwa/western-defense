# Wiki de Entidades — índice navegable

> **Este archivo es generado.** Se produce con
> `python3 tools/wiki_to_resources.py --emit-index`.
> La **fuente canónica** es [`docs/WIKI.md`](../WIKI.md): editá las fichas ahí
> y regenerá este índice. No edites este archivo a mano.

Documentos hermanos: [GDD](../GDD.md) · [TECH](../TECH.md) ·
[esquema de ficha](../WIKI.md#0-instrucciones-para-sistemas-de-ia)

## Cómo leer esta wiki

- Cada entidad es una **ficha YAML** con esquema fijo (WIKI §0). El campo `id`
  (snake_case) es el identificador canónico: se usa para nombres de archivo,
  clases, claves de datos y referencias cruzadas.
- `estado: canon` = decidido. `estado: propuesta` = pendiente de validar en
  prototipo.
- Los campos **`TBD`** están pendientes de balance y **no se inventan**
  (CLAUDE.md, regla 4). La columna *TBD* de las tablas cuenta cuántos tiene
  cada ficha.
- Regla de diseño de todo enemigo: **quiere llevarse algo** — qué roba, cómo
  lo roba, cómo se evita.
- De la wiki salen los datos del juego vía
  [`tools/wiki_to_resources.py`](../../tools/wiki_to_resources.py) → `data/`.

---

## Unidades del jugador

→ [Sección completa](../WIKI.md#1-unidades-del-jugador)

| Ficha | Nombre | Rol | Obtención | Estado | TBD |
| --- | --- | --- | --- | --- | --- |
| [`peon`](../WIKI.md#11-peon) | Peón | economico | Recluta base en la Taberna | ✅ canon | 3 |
| [`pistolero`](../WIKI.md#12-pistolero) | Pistolero | defensivo | Peón + revólver fabricado en la Armería | ✅ canon | 6 |
| [`cazador`](../WIKI.md#13-cazador) | Cazador | mixto | Peón + rifle largo | ✅ canon | 4 |
| [`chatarrero`](../WIKI.md#14-chatarrero) | Chatarrero (Scavenger) | economico | Peón + mejora en el Laboratorio | ✅ canon | 3 |
| [`vaquero_ganado`](../WIKI.md#15-vaquero_ganado) | Vaquero de ganado | mixto | Peón + Establo construido | 🧪 propuesta | 5 |
| [`cientifico`](../WIKI.md#16-cientifico) | Científico / Profesor | investigacion | Llega al pueblo al alcanzar cierto nivel/renombre, o se encuentra explorando | ✅ canon | 1 |
| [`dinamitero`](../WIKI.md#17-dinamitero) | Dinamitero | defensivo | Recluta especial / edificio minero (por definir) | 🧪 propuesta | 4 |
| [`doctor`](../WIKI.md#18-doctor) | Doctor / Curandero | economico | Recluta especial | 🧪 propuesta | 4 |
| [`sheriff`](../WIKI.md#19-sheriff) | Sheriff | defensivo | Evento / nivel de pueblo alto | 🧪 propuesta | 5 |

## Enemigos

→ [Sección completa](../WIKI.md#2-enemigos)

### LADRON

→ [Sección completa](../WIKI.md#21-categoría-ladron)

| Ficha | Nombre | Qué roba | Movimiento | Aparición | Estado | TBD |
| --- | --- | --- | --- | --- | --- | --- |
| [`ratero_gris`](../WIKI.md#211-ratero_gris) | Ratero Gris | recursos | terrestre | noche 1+ | ✅ canon | — |
| [`coyote_plateado`](../WIKI.md#212-coyote_plateado) | Coyote Plateado | comida | terrestre | noche 2+ | ✅ canon | 1 |
| [`manos_largas`](../WIKI.md#213-manos_largas) | Manos Largas | recursos | terrestre | noche 4+ | ✅ canon | 1 |

### ABDUCTOR

→ [Sección completa](../WIKI.md#22-categoría-abductor)

| Ficha | Nombre | Qué roba | Movimiento | Aparición | Estado | TBD |
| --- | --- | --- | --- | --- | --- | --- |
| [`platillo_sonda`](../WIKI.md#221-platillo_sonda) | Platillo Sonda | ganado | volador | noche 3+ | ✅ canon | — |
| [`platillo_abductor`](../WIKI.md#222-platillo_abductor) | Platillo Abductor | personas | volador | noche 6+ | ✅ canon | — |
| [`sombrero_negro`](../WIKI.md#223-sombrero_negro) | Sombrero Negro | personas | terrestre | noche 7+ | ✅ canon | — |

### TANQUE

→ [Sección completa](../WIKI.md#23-categoría-tanque)

| Ficha | Nombre | Qué roba | Movimiento | Aparición | Estado | TBD |
| --- | --- | --- | --- | --- | --- | --- |
| [`toro_de_marte`](../WIKI.md#231-toro_de_marte) | Toro de Marte | nada (rompe) | terrestre | noche 5+ | ✅ canon | — |
| [`caparazon`](../WIKI.md#232-caparazon) | Caparazón | nada (rompe) | terrestre | noche 8+ | ✅ canon | — |
| [`demoledor`](../WIKI.md#233-demoledor) | Demoledor | nada (rompe) | terrestre | noche 9+ | ✅ canon | — |

### SOPORTE

→ [Sección completa](../WIKI.md#24-categoría-soporte)

| Ficha | Nombre | Qué roba | Movimiento | Aparición | Estado | TBD |
| --- | --- | --- | --- | --- | --- | --- |
| [`psiquico_velado`](../WIKI.md#241-psiquico_velado) | Psíquico Velado | nada (potencia) | terrestre | noche 8+ | ✅ canon | — |
| [`reparador`](../WIKI.md#242-reparador) | Reparador | nada (potencia) | volador | noche 9+ | ✅ canon | — |
| [`hipnotizador`](../WIKI.md#243-hipnotizador) | Hipnotizador | nada (potencia) | terrestre | noche 10+ | ✅ canon | — |
| [`faro_lunar`](../WIKI.md#244-faro_lunar) | Faro Lunar | nada (potencia) | terrestre | solo luna llena | ✅ canon | — |

### JEFE

→ [Sección completa](../WIKI.md#25-categoría-jefe)

| Ficha | Nombre | Qué roba | Movimiento | Aparición | Estado | TBD |
| --- | --- | --- | --- | --- | --- | --- |
| [`nave_capataz`](../WIKI.md#251-nave_capataz) | Nave Capataz | personas y ganado (masivo) | volador | lunas llenas (mini-jefe recurrente) | ✅ canon | — |
| [`el_ganadero`](../WIKI.md#252-el_ganadero) | El Ganadero | nada (rompe) — pero su nombre es la amenaza | terrestre | evento mid-game (noche ~10, por definir) | 🧪 propuesta | 1 |
| [`nave_nodriza`](../WIKI.md#253-nave_nodriza) | Nave Nodriza | n/a — es el OBJETIVO FINAL, no ataca el pueblo | estatica (campo cercano, visible desde el inicio del run) | presente desde la noche 1 (meta visible) | ✅ canon | 1 |

## Componentes (drops)

La tabla canónica de componentes vive en [WIKI §3](../WIKI.md#3-registro-de-componentes-drops). Los componentes son la moneda del árbol tecnológico ([GDD §8](../GDD.md#81-árbol-tecnológico-in-run)).

## Estado de completitud

- **25** fichas (9 unidades, 16 enemigos).
- **5** en `estado: propuesta` — pendientes de validar: `vaquero_ganado`, `dinamitero`, `doctor`, `sheriff`, `el_ganadero`.
- **13** fichas con campos `TBD` pendientes de balance (39 campos en total).
