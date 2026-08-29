# COWBOY DEFENSE — Game Design Document v0.4

> **Estado:** Cuarto borrador · **Fecha:** Agosto 2026 · **Equipo:** 2 personas + sistemas agénicos
> **Documentos hermanos:** [`WIKI.md`](WIKI.md) (fuente canónica de unidades y enemigos) · [`TECH.md`](TECH.md) (documento técnico) · [índice navegable de la wiki](wiki/README.md)
> **Nombre tentativo:** Cowboy Defense (working title)

> ### ⚠️ v0.4 — cambia el núcleo defensivo
> **No hay muros.** La invasión es una sorpresa: el rancho está abierto, los
> aliens bajan de sus naves y caminan hasta lo que quieren. La defensa deja de
> ser un perímetro y pasa a ser **edificios que de noche se vuelven refugio o
> defensa**, más **torres colocables** que castigan al alien mientras roba.
> Los muros estilo *Kingdom* siguen sobre la mesa como **variante opcional**, y
> su versión de late-game es un **campo de fuerza alien**, no una empalizada.
> Lo tocado: §3.1, §5, §6 entero, §7, §8.1, §10 y §13. Las fichas canónicas
> están en [`WIKI.md`](WIKI.md); las **decisiones que siguen abiertas** están en
> §13 y ninguna se resuelve sin Mato.

> ### ⭐ 29 de agosto de 2026 — el héroe tiene clase
> Mato definió **tres clases de héroe**: **Sheriff** (ataque), **Alcalde**
> (economía) y **Carpintero** (defensa y capacidad). Una clase = un eje, se
> elige al empezar la run, y son además el **marco de la meta-progresión
> roguelite**: los puntos de fin de run se gastan en mejorar tu héroe o
> desbloquear héroes nuevos dentro de esas tres clases. Lo tocado: §4.3 (nuevo)
> y §8.3. Fichas canónicas en [`WIKI.md §11`](WIKI.md#11-clases-del-héroe);
> las magnitudes de los bonus son `TBD` de balance.

---

## 1. Visión General

### 1.1 Elevator Pitch
Un tower defense de scroll lateral 2D ambientado en el Viejo Oeste (1870s, Weird West). De día exploras el desierto y gestionas tu rancho con control indirecto; de noche, alienígenas atacan para **robarte** — gente, ganado, recursos. Cada cosa que te roban te debilita para el día siguiente. Recuperas tecnología alienígena de los enemigos caídos para mejorar tus armas y torres, hasta poder marchar contra la nave nodriza y liberar el valle.

### 1.2 Género
Tower Defense + gestión de recursos + roguelike, con control indirecto tipo *Kingdom*.

### 1.3 Referencias principales
| Juego | Qué tomamos |
|---|---|
| **Kingdom: New Lands / Two Crowns** | Control indirecto, scroll lateral, economía de día / defensa de noche, expansión de territorio, minimalismo, tensión sin horror explícito |
| **Dome Keeper** | Ciclo recolección/defensa contra reloj, decisión constante entre mejorar economía o defensa, runs de roguelike |
| **They Are Billions / RTS clásicos** | Reparación activa de estructuras durante el ataque |

### 1.4 Hook diferenciador
Los enemigos **no destruyen: roban.** El fallo no es binario (game over instantáneo) sino una espiral: cada noche mala te quita brazos, comida y defensas para la siguiente. Pierdes cuando la espiral te alcanza. Y el arco de poder es irónico: terminas defendiéndote de los aliens **con sus propias armas**.

Desde v0.4 el robo es más concreto y más doloroso: no te roban *por encima de un muro*, te roban **de adentro de tus edificios**. Cada alien entra al refugio más cercano y tarda en sacar lo que hay — **3–5 s por cosa**, sea un aldeano, comida o una vaca; los aliens grandes se llevan **dos** y tardan más. No podés impedir que entren; podés cobrarles esos segundos.

Y el arco irónico también tiene un bucle diario: **de mañana salís a barrer los restos**. Lo que derribaste de noche es lo que juntás de día — comida y **piezas alien** (§5.1), la moneda de todas las mejoras.

### 1.5 Pilares de diseño
1. **El robo duele más que la muerte** — todo lo que tienes es robable; proteger es priorizar.
2. **Cada noche te transforma** — la partida es una carrera entre tu progresión y su escalada.
3. **Cómico pero inquietante** — tono de cómic pulp; el miedo viene de la incertidumbre (¿qué hay en el bosque? ¿qué trae la luna llena?), no del gore.
4. **Sus armas son tu salvación** — la tecnología alienígena es el recurso de progresión central.

---

## 2. Especificaciones Técnicas

| Aspecto | Decisión |
|---|---|
| Plataformas | PC (Steam) primero; consola después. Móvil descartado por ahora |
| Input | Gamepad como input primario; teclado soportado |
| Perspectiva | 2D side-scroller, un solo eje horizontal (izquierda ↔ derecha) |
| Multijugador | **Coop local 2 jugadores desde el diseño inicial** (split screen). Sin online |
| Arte | Pixel art |
| Motor | **Godot 4 + C#** (recomendado). Alternativa: Unity 2D. Ver Anexo A |
| Equipo | 2 devs con experiencia + workflows agénicos; escalable |

---

## 3. Core Loop

### 3.1 Ciclo día/noche (duración fija)

```
AMANECER ──► DÍA ──────────────► ATARDECER ──► NOCHE ──────────► AMANECER
  Aliens      Explorar, recolectar,  Última        Oleadas atacan     Aliens huyen
  huyen con   construir, investigar, oportunidad   y ROBAN. Defensa   con lo robado.
  lo robado   reclutar, expandir     de replegarse y reparación       Balance de daños
  BARRIDO
  de restos
```

- **Amanecer — el barrido de restos (v0.5):** apenas hay luz, la gente sale a levantar lo que dejó la noche. Traen **comida** y **piezas de las naves y los aliens caídos** ([`pieza_alien`](WIKI.md#73-pieza_alien)). Es la recompensa material de haber peleado bien: **cuantos más derribaste de noche, más juntás de mañana** — y al revés, una noche mala te cuesta dos veces, porque perdés gente *y* no hay qué barrer. Las piezas son la moneda de todas las mejoras post-científico (§8.1).
- **Día (duración fija):** los trabajadores recolectan en el rango cercano al pueblo; el jugador cabalga a explorar más lejos, encuentra recursos, sitios de interés y reclutas.
- **Atardecer:** la última oportunidad de replegarse tiene ahora un contenido concreto — los trabajadores entran a los **edificios-refugio** y los vaqueros guardan las vacas en el establo. Lo que quede afuera, queda afuera.
- **Noche (duración fija):** oleadas de aliens entran por **izquierda y derecha**; más adelante, **naves por arriba**. Cada alien va al edificio-refugio más cercano que tenga lo que busca y **se queda adentro robando** durante unos segundos. Torres y unidades pelean solas y aprovechan esa ventana. El jugador reposiciona, gasta recursos de emergencia y los reparadores mantienen en pie torres y edificios.
- **Excepción — días especiales:** con aviso previo, puede ocurrir un ataque diurno con enemigo/jefe especial (evento raro, telegráfiado).

### 3.2 Loop de una run (roguelike, 30–60 min)
1. Empiezas con el town center, 2–3 unidades y recursos mínimos.
2. Sobrevives noches de dificultad creciente, moduladas por el **ciclo lunar** (§9).
3. Acumulas tecnología alienígena → desbloqueas armas → armas mejores → sobrevives noches peores.
4. **Victoria:** cuando tu fuerza lo permite, armas una partida de asalto (héroe + milicia con armas alien) y marchas de día hacia la **base alienígena / nave nodriza** en un campo cercano, y la destruyes.
5. **Derrota:** una noche los aliens simplemente te arrasan — te raptaron tanta gente en noches anteriores que ya no puedes defenderte. No hay "corona": la derrota es la culminación de la espiral de robos.
6. Al terminar (ganes o pierdas), obtienes **puntos de meta-progresión** (§8.3).

### 3.3 Diseño del pacing del run (propuesta a validar en prototipo)
- Objetivo: run ganable en **~12–15 noches** a ~3–4 min por ciclo día+noche ≈ 45–55 min.
- Noches 1–3: onboarding suave (solo Ladrones). Noches 4–7: aparecen Abductores y primer Tanque. Noches 8+: composiciones mixtas, Soporte, mini-jefes en lunas llenas.
- La nave nodriza se revela en el mapa desde temprano (como los portales de Kingdom): el jugador siempre sabe cuál es la meta.

### 3.4 Estructura del mapa (definido)
- **Prototipo / v1:** un solo mapa fijo en su layout jugable (posición del town center, flancos, distancia a la nodriza), pero con **generación semi-aleatoria por run** de:
  - el **fondo/paisaje** (composición del escenario, posiblemente con herramientas de arte generativo como apoyo de pipeline),
  - la **ubicación de recursos** (árboles, sitios de chatarra, puntos de caza, reclutas).
- Objetivo: que cada run se sienta distinta sin el costo de mapas hechos a mano ni proceduralidad compleja.
- **Post-v1 (visión):** en lugar de "islas" como Kingdom New Lands, la progresión geográfica son **otros pueblos y ciudades más grandes** — asentamientos nuevos con sus propios retos, escalando de rancho → pueblo → ciudad. Cada asentamiento funcionaría como un "mundo" del roguelike.

---

## 4. Controles y Personaje

- **Control indirecto tipo Kingdom:** el jugador maneja a su ranchero a caballo. No apunta ni dispara manualmente: el personaje **dispara automáticamente** a enemigos en rango.
- Acciones del jugador: moverse, soltar recursos/órdenes (marcar construcción, reclutar, asignar rol), activar edificios, liderar la partida de asalto final.
- Las unidades y torres actúan por IA propia.

### 4.1 Sistema de derribo del héroe (definido)
El héroe nunca muere ni es raptado — se degrada en dos estados:

| Estado | Trigger | Efecto |
|---|---|---|
| **Derribado** | Recibe suficiente daño | Aturdido brevemente en el suelo; al levantarse queda **Malherido** |
| **Malherido** | Tras el derribo | Puede actuar, pero **mucho más lento** (movimiento, cadencia de disparo). Recuperación al amanecer o vía Doctor |
| **Fuera de combate** | Es derribado de nuevo estando Malherido | El personaje **deja de operar**. El jugador conserva control total de la cámara y **observa si sus defensas sobreviven solas** el resto de la noche |

- Intención de diseño: el castigo por arriesgar al héroe no es un game over, sino perder tu agencia — la noche se vuelve "cosechas lo que sembraste". Refuerza el pilar de que las defensas y unidades deben poder sostenerse sin microgestión.
- **Recuperación tras Fuera de combate (definido):** el héroe permanece caído donde quedó hasta el **amanecer**; revive Malherido en ese punto y debe volver al pueblo. No hay penalización adicional de recursos — el costo real es la noche que pasaste sin operar y el trayecto de regreso.

### 4.2 Cooperativo local (definido)
- **2 jugadores en coop local desde el inicio del desarrollo**, referencia directa: *Kingdom Two Crowns*.
- **Split screen dinámico:** la pantalla se divide cuando los jugadores se alejan y **se une cuando están cerca**.
- Solo local (misma máquina / mismo sofá). **Sin multiplayer en línea** — fuera de alcance.
- Ambos héroes comparten economía y pueblo; cada uno tiene su propio estado de derribo (§4.1).
- **Fuera de combate en coop (definido):** si un jugador queda Fuera de combate lejos del pueblo (ej. explorando el bosque de noche), **permanece caído donde quedó hasta el amanecer**; ahí revive Malherido y debe regresar al pueblo por su cuenta. El otro jugador sigue jugando normalmente. Si esto ocurre en plena defensa nocturna, el pueblo pelea con un héroe menos — el castigo es orgánico, no scripted. Si ambos caen, ambos observan hasta el amanecer.
- Implicación técnica: todos los sistemas (cámara, HUD, órdenes, recolección) se diseñan desde el día uno asumiendo 1–2 héroes, no se parchea después.

### 4.3 Clases del héroe (definido)
Decidido por Mato (29 de agosto de 2026). El héroe deja de ser un ranchero genérico: **al empezar cada run elegís una de tres clases**, y cada clase mejora **un solo eje** del rancho.

| Clase | Bonus | Qué cambia en la partida |
|---|---|---|
| **Sheriff** | **Ataque** | Sube el daño de tus **edificios** (torres y edificios en modo defensa) y de tus **unidades**. La ventana de robo (§6.3) se cierra antes: matás al alien cargado y suelta el botín |
| **Alcalde** | **Economía** | Sube la **producción de recursos** — comida, madera, chatarra, la cadena del ganado (§5.4) y el barrido del amanecer. No evita el robo: hace que reponerlo cueste menos noches |
| **Carpintero** | **Defensa y capacidad** | Sube la **defensa de tus recursos** (los edificios aguantan más y al alien le cuesta más sacarles algo) y la **capacidad** de los edificios: entra más gente, ganado y recursos al refugio |

- **Una clase = un eje.** El Sheriff no toca la economía, el Alcalde no dispara mejor, el Carpintero no sube el daño. Elegir clase es elegir **por qué lado peleás la espiral del robo** (§5.3): matarlos antes, reponer más rápido, o que te saquen menos y te quepa más.
- **Coop (§4.2):** cada jugador elige su clase y los bonus se aplican sobre el mismo rancho compartido. Sheriff + Carpintero se lee natural —uno estira la ventana de robo, el otro la aprovecha—; cómo se apilan **dos clases iguales** es balance pendiente.
- **Los números no están decididos.** La magnitud de cada bonus y su escalado por nivel son `TBD` (no se inventan): las fichas canónicas están en [`WIKI.md §11`](WIKI.md#11-clases-del-héroe), en `estado: propuesta`.
- Las clases son además el **marco de la meta-progresión** entre runs (§8.3).
- Pendiente de ficción: la unidad reclutable *Sheriff* ([wiki §1.9](WIKI.md#19-sheriff)) sigue existiendo y comparte nombre con la clase — hay que desambiguar.

---

## 5. Recursos y Economía

### 5.1 Recursos (sin oro — decisión tentativa)
| Recurso | Fuente | Uso | Robable |
|---|---|---|---|
| **Madera** | Árboles del entorno (taladores) | Construcción y expansión de edificios y torres | Sí |
| **Chatarra / Tec. alienígena** — las [`piezas alien`](WIKI.md#73-pieza_alien) | **El barrido del amanecer** (§3.1): restos de aliens y naves derribadas la noche anterior. También sitios de crash y hallazgos del desierto | Investigación, armas, torres avanzadas y **todas las mejoras post-científico** (§8.1) | Sí |
| **Comida** | Ganado (**ya no es pasivo**, §5.4), caza, cultivos | Mantiene a la población. Sin comida → la gente muere/deserta en ~2 días | Sí (¡y el ganado también!) |
| **Pasto** | Crece de día alrededor de la granja; parches naturales en el mapa | Alimenta al ganado. Es el único recurso que **no** se almacena: se produce y se consume en el sitio | No — pero perderlo te mata las vacas igual |
| **Población** | Reclutas encontrados/atraídos | Es el recurso vivo: trabajan, pelean, investigan | **Sí — es lo que más roban** |

- Chatarra y tecnología alien son **el mismo recurso**: recoges tec alien y la refinas/mejoras.
- Nota de diseño: si en prototipo la economía pide una moneda blanda universal, se reevalúa el oro.

### 5.4 La cadena del ganado (v0.4)
El ganado dejó de ser un número que sube solo. Ahora es una cadena de tres eslabones, y cada uno se puede cortar:

```
GRANJA ──produce──► PASTO ──lo pasta──► VACA ──produce──► COMIDA
```

- **De día** los vaqueros sacan las vacas a pastar el pasto que crece alrededor de la granja y el establo. **Más vacas = el pasto se consume más rápido.**
- Si el rebaño crece más rápido que las granjas, las vacas **pasan hambre** y dejan de producir comida. Escalar ganado obliga a escalar granjas: tener muchas vacas es una decisión con costo, no una acumulación gratis.
- **De noche** las vacas se guardan en el establo. Adentro están a salvo del rayo tractor, pero concentradas: un ladrón que entre las encuentra a todas juntas.
- Fichas canónicas: [`pasto`](WIKI.md#71-pasto) y [`vaca`](WIKI.md#72-vaca) (WIKI §7). Los ritmos de crecimiento y consumo son `TBD` — es justamente lo que hay que balancear.
- **Segunda forma de perder ganado:** ya no solo te lo roban; también se te muere de a poco porque construiste mal. Es la espiral del robo aplicada a la economía propia.

### 5.2 Transporte físico de recursos
- Los recursos **existen físicamente**: aparecen en el mundo, un trabajador los carga y los deposita en el almacén/edificio correspondiente.
- Consecuencia clave: los recursos en tránsito son vulnerables. Si un abductor se lleva una vaca y **derribas la nave a tiempo, la vaca cae viva** y la recuperas. Si la nave sale de pantalla / termina la noche: **se perdió para siempre.** No hay rescate posterior.

### 5.3 La espiral del robo (mecánica central)
- Te roban vacas → mañana produces menos comida → alimentas menos gente → menos defensores → la próxima noche te roban más.
- El día siguiente a una mala noche es de **recuperación**: decidir si reponer comida, reponer gente o reforzar defensa es el corazón estratégico del juego.

---

## 6. El Rancho (Base)

### 6.1 Layout — el rancho abierto (v0.4)
- **Layout fijo con slots de mejora.** Centro: **Town Center**. A los lados, slots de edificios de economía.
- **No hay línea de muros.** La ficción lo explica: esto es un valle del oeste en 1870, no un castillo bajo asedio anunciado. Nadie levantó una muralla porque nadie sabía que venía nadie; los aliens bajan de las naves y caminan hasta lo que quieren.
- **Las torres se colocan libres**, donde el jugador quiera. Elegir a qué edificio cubre cada torre es *la* decisión táctica de la noche.
- El territorio se sigue pudiendo **expandir** a más slots y más recursos — pero expandirse ya no significa empujar un muro, significa tener más edificios sueltos que cubrir.
- **No hay muros, y no hay variante con muros** (decidido, §13.1 D2). Los aliens **se mueven, entran y disparan libremente**: nada les impide llegar. Gente, vacas y recursos se refugian en los edificios que los admiten, o en el Town Center. Los muros estilo *Kingdom* quedaron descartados; la [`barricada`](WIKI.md#58-barricada) está archivada.

### 6.2 Edificios — dos vidas, día y noche (v0.4)

> ⚠️ Fichas canónicas en [`WIKI.md §5`](WIKI.md#5-edificios); las reglas normativas del ciclo día/noche están en [WIKI §5.0](WIKI.md#50-reglas-de-los-edificios-de-noche-cambio-canónico).

**La regla nueva:** todo edificio cumple su función económica de día y **al caer la noche se convierte en refugio o en defensa**. El edificio dejó de ser decorado: de noche *es* el sistema defensivo.

| Edificio | De día | De noche |
|---|---|---|
| **Town Center** | Núcleo y almacén principal. Nivel del pueblo = desbloqueos | Refugio principal — el que más gente y más recursos tiene adentro |
| **Taberna / Inn** | Atrae y aloja reclutas; asignación de roles | Refugio de personas — el objetivo más goloso por densidad de gente |
| **Establo / Corral** | Los vaqueros sacan las vacas a pastar; el ganado convierte pasto en comida | Refugio de ganado — se guardan las vacas y se espera la invasión |
| **Granja / Granero** | Cultiva comida **y hace crecer el pasto a su alrededor** (§5.4) | Refugio de gente y de la comida almacenada |
| **Armería / Herrería** | Fabrica y mejora armas humanas; equipa unidades | Refugio; es el candidato natural a la rama *refugio+defensa* — ya tiene las armas adentro |
| **Laboratorio del Profesor** | El científico investiga tec alien; árbol tecnológico | Refugio del científico y de los componentes sin investigar |
| **Torre de vigilancia** | Vigila el horizonte y revela infiltrados | **Defensa** — dispara, incluso a quien está robando adentro de un edificio. Se coloca libre y se configura (§6.3) |
| **Campo de fuerza alien** | Inactivo, recargando | **Defensa T3** — barrera de energía entre emisores. La respuesta alien al muro (§8.1) |
| ~~**Barricadas / Muros**~~ | — | **Archivada** (§13.1 D2): el juego no tiene muros, ni siquiera como variante |

### 6.3 Defensa sin muros: la ventana de robo (v0.4)

El sistema defensivo entero se apoya en una sola idea: **robar lleva tiempo, y ese tiempo es tuyo.**

1. El alien entra al **primer edificio-refugio de su camino** que tenga lo que busca.
2. Adentro, saca las cosas de a una: **3–5 s cada una**, sea un **aldeano**, **comida** o una **vaca** — el mismo rango para las tres (§13.1 D3). El valor se sortea dentro del rango **una vez por oleada**, no por robo, así que el jugador aprende el ritmo de la noche.
3. **Los aliens grandes se llevan dos cosas** en vez de una, y tardan más en hacerlo. El multiplicador exacto es `TBD` (balance), igual que qué enemigo cuenta como grande.
4. Mientras carga es un **blanco quieto**. Matarlo antes de que termine **cancela el robo**; matarlo cargado le hace **soltar lo robado ahí mismo** — la misma regla que derribar un abductor en el aire.
5. No impedís que entren. Les cobrás los segundos que pasan adentro.

**Torres colocables y configurables.** Las torres ya no viven en una línea: se colocan donde el jugador quiera, y cada una expone una **prioridad de objetivo**:

| Prioridad | A quién le dispara primero | Para qué sirve |
|---|---|---|
| **Primero en llegar** | Al que entró antes al alcance | Corta el goteo, defensa pareja |
| **Más cercano a los recursos** | Al que está por alcanzar un refugio | Preventivo: no llegan a empezar |
| **El que ya carga** | Al que ya lleva algo encima | Recupera botín; la respuesta a *Manos Largas* |

**Los aliens atacan las torres primero — variante A** (decidido, §13.1 D1). La torre no es un espectador: el alien que se engancha con ella **la resuelve antes** de seguir al refugio. Tres consecuencias:

- **Colocar una torre es elegir dónde se pelea**, y no solo a qué refugio cubrís. Adelantada compra tiempo lejos del botín; pegada al refugio pelea encima de la gente.
- **La torre es gastable:** puede caer, y sostenerla de noche cuesta un reparador expuesto.
- **El *Caparazón* funciona como escudo móvil** — existe para comerse ese fuego mientras los ladrones pasan detrás.

No se pidió que fuera configurable por dificultad ni por tipo de enemigo: variante A es el comportamiento único del juego.

**Reparación.** Se mantiene la reparación activa estilo RTS, con el blanco cambiado: un trabajador puede reparar **torres y edificios** *mientras* reciben daño (riesgo: el reparador es raptable, y de noche está fuera del refugio). Torres y edificios se construyen/mejoran también durante la noche si hay recursos y manos.

**Lo que no cambia.** Los ataques por ambos flancos obligan a repartir defensa; las naves aéreas (mid-game) obligan a tener antiaéreo.

### 6.4 Desbloqueos por objetivos (v0.4)
- Algunas entidades no se compran ni se investigan: **se ganan cumpliendo un objetivo del rancho.** El caso canónico: **el científico llega cuando sostenés X vacas vivas.**
- Es la manera del juego de decir que criar ganado *también* es progresión tecnológica: el ranchero que prospera atrae a la gente que lo hace prosperar más.
- **El científico es la bisagra del run** (§13.1 D5): su llegada **abre las mejoras**, y todas las mejoras se pagan en piezas alien. Antes de él las piezas se acumulan sin uso.
- **La curva de checkpoints está aprobada** (§13.1 D4, 29 de agosto de 2026). El científico no llega por un número suelto de vacas: llega al final de **cuatro compuertas** que hay que cumplir en orden, cada una sobre un eje distinto y cada una abriendo algo visible:
  1. **C1 — sobrevivencia:** sostener un rebaño chico. Abre la lectura de la curva: el tablón del Town Center con las cuatro compuertas.
  2. **C2 — comunidad:** sostener la población sin que te vacíen la taberna. Abre **el doctor** — *"para que pueda sobrevivir hasta el final"*.
  3. **C3 — capacidad económica:** juntar piezas alien en el barrido del amanecer. Amplía el barrido: más piezas por derribo y alcance a los restos lejanos.
  4. **C4 — sobrevivencia otra vez, pero bajo fuego:** sostener un rebaño grande, con C1–C3 ya cumplidas. Abre **el científico**, y con él todas las mejoras.
  Lo aprobado es la **forma**: cuántas vacas, cuánta gente y cuántas piezas siguen `TBD` y salen del prototipo. Tabla canónica en [`WIKI.md §8.1`](WIKI.md#81-curva-de-progresión-del-científico--canon-d4-aprobada-por-mato).
- **El jugador ve la curva mientras juega.** Un tablón en el Town Center: la compuerta cumplida tachada, la actual con barra y número, las futuras con título visible y cifra en gris. Se resuelve **al amanecer**, nunca en mitad de la noche, y avisa tanto cuando falta poco como **cuando retrocedés** por un robo — que es el hook del juego dicho por la UI. Una compuerta cumplida no se pierde; lo que se reinicia es la ventana de sostenimiento de la que está en curso.
- El patrón es extensible — otras unidades y edificios pueden colgar de objetivos propios (el `sheriff` sigue siendo candidato, `TBD`), y el **campo de fuerza** ya cuelga de uno: científico + X piezas alien.
- Tabla canónica de objetivos: [`WIKI.md §8`](WIKI.md#8-objetivos-de-desbloqueo). Todavía **no son un tipo de ficha**: son una tabla, y volverlos entidades está en el backlog.

### 6.5 Niveles de edificio — un árbol de talentos por edificio (v0.4)

**Cada edificio tiene su propio árbol de talentos** (decidido, §13.1 D6). Se abre **clickeando el edificio**, y lo que comprás ahí vale para *ese* edificio y para ningún otro — ni siquiera para otro del mismo tipo. No hay árbol global: la progresión **es** la estrategia de layout del jugador.

La primera bifurcación de ese árbol son las dos ramas canónicas, y son excluyentes:

```
        NIVEL 1 · refugio
        ├── refugio + defensa → sigue guardando gente, y además dispara
        └── doble refugio     → no dispara, pero duplica la capacidad
```

- Es una **elección, no una escalera**: el mismo edificio no puede ser fortín y granero a la vez.
- *Refugio + defensa* convierte ese edificio en un punto que se aguanta solo; *doble refugio* concentra más en menos lugares — menos edificios que cubrir, más huevos en la misma canasta.
- Dos graneros del mismo pueblo pueden ir por caminos distintos, y esa es la gracia.
- **Las mejoras se pagan con piezas alien** y se abren con el científico (§6.4, §8.1).
- El contenido del árbol más allá de la primera bifurcación, sus costos y qué edificios pueden tomar cada rama son `TBD`.

---

## 7. Unidades del Jugador (Wiki — propuesta inicial)

> ⚠️ **Fuente canónica: [`WIKI.md`](WIKI.md#1-unidades-del-jugador)** ([índice](wiki/README.md#unidades-del-jugador)). Las tablas de este documento son el resumen de diseño; las fichas completas, stats y drops viven en la wiki.

> Todas las unidades son **raptables**. Perder una unidad no es solo perder DPS: es perder su función económica. Desde v0.4, de noche la gente está **dentro de los edificios-refugio** — sacarla de ahí le cuesta al alien 1–3 s por persona (§6.3).

| Unidad | Rol | Cómo se obtiene | Notas |
|---|---|---|---|
| **Peón** | Recolecta madera/chatarra, construye, repara | Recluta base (Taberna) | La sangre del pueblo. Objetivo favorito de los Ladrones |
| **Pistolero** | Defensa básica a distancia | Peón + revólver (Armería) | Evoluciona con armas del árbol tec |
| **Cazador** | Genera comida de día; francotirador de noche | Peón + rifle | Largo alcance, cadencia lenta. Bueno contra voladores |
| **Chatarrero (Scavenger)** | Especialista en recoger tec alien del campo y de la batalla | Peón + mejora en Laboratorio | Recoge más rápido y más lejos; clave para el árbol tec |
| **Vaquero de ganado** | Lleva las vacas al pasto de día (§5.4) y las guarda en el establo de noche; lazo | Peón + Establo | Puede **enlazar** aliens pequeños o jalar de vuelta ganado abducido (a validar). Cuántas vacas saca a pastar es una decisión: más comida hoy, menos pasto mañana |
| **Científico / Profesor** | Investiga tecnología alien; desbloquea armas | **Objetivo de desbloqueo: llega cuando sostenés X vacas** (§6.4; X es `TBD`). También se encuentra explorando | No pelea. Si te lo raptan, la investigación se detiene |
| **Dinamitero** | Daño en área | Recluta especial / edificio minero | Riesgo: fuego amigo cómico |
| **Doctor / Curandero** | Cura unidades entre noches; revive derribados | Recluta especial | Weird West: elixires dudosos |
| **Sheriff** | Mini-héroe defensivo, buff de moral en su zona | Evento / nivel de pueblo | Ancla un flanco |

**Por discutir:** ¿unidades con arma alien son una clase nueva ("Fusilero de plasma") o una mejora de equipo sobre el Pistolero? (Propuesta: mejora de equipo — menos sprites, más combinatoria.)

---

## 8. Armas, Tecnología y Progresión

### 8.1 Árbol tecnológico (in-run)
- Eje de progresión: **armas humanas → híbridas → alienígenas**.
- Flujo: los aliens derribados / naves caídas sueltan **componentes** → los Chatarreros los recogen → el Científico los investiga en el Laboratorio → se desbloquea la receta → se fabrica pagando chatarra/madera.
- Ejemplo de cadena: consigues un *difusor de luz* de un alien → investigación → desbloquea **Bomba de gas lumínico** → los scavengers juntan los componentes → se fabrica y se monta en torre.
- Tiers tentativos:
  - **T1 Humano:** revólver, rifle, escopeta, dinamita, torre Gatling.
  - **T2 Híbrido:** balas recubiertas de aleación alien, gatling sobrecargada, trampas de pulso.
  - **T3 Alien:** rifle de plasma, torre de rayo, bomba de gas lumínico, **barrera de energía** (el [campo de fuerza alien](WIKI.md#59-campo_fuerza_alien) — la respuesta del juego a "quiero un muro": no una empalizada de madera, sino la misma tecnología con la que te robaron), arpón antigravedad (baja naves).
- El campo de fuerza llega **tarde a propósito**: si estuviera disponible temprano mataría la tensión del rancho abierto (§6.1). Si es una estructura o un arma montable en torre es una decisión abierta (§13).

### 8.2 Captura de tecnología, no de aliens
- **No hay captura de aliens vivos** (descartado). Toda la tec viene de restos y sitios de crash.

### 8.3 Meta-progresión (entre runs)
- Al final de cada run (victoria o derrota) ganas **puntos** según noches sobrevividas, tec investigada, jefes derrotados, gente salvada.
- Se gastan en mejoras permanentes tipo roguelike: tecnologías pre-desbloqueadas, +daño del héroe, empezar con una unidad extra, descuentos, nuevos edificios disponibles, etc.
- **El eje principal del meta son las tres clases del héroe (§4.3).** Los puntos se gastan en dos cosas:
  - **Mejorar tu héroe** — subir el bonus de su clase (más ataque para el Sheriff, más producción para el Alcalde, más defensa/capacidad para el Carpintero) y abrir perks propios de esa clase.
  - **Desbloquear héroes nuevos** — personajes distintos que **pertenecen a una de las tres clases**. Las clases son el marco fijo; los héroes, el contenido que crece. Un héroe nuevo trae el bonus de su clase con su propio sabor (arma inicial, perk, ficción), no un cuarto eje.
- Al empezar la run elegís **con qué héroe desbloqueado jugás**, y eso fija tu clase para toda la partida. En coop cada jugador elige el suyo (§4.2).
- **Por definir:** nombre/ficción de estos puntos (¿"Renombre"? ¿"Recortes de periódico"?), el tamaño del árbol meta, y **cuántos héroes por clase** (hoy la clase es el arquetipo y el héroe es genérico — las fichas de héroe concreto todavía no existen).

---

## 9. Escalada de Dificultad — El Ciclo Lunar

- La dificultad escala **por noche** (más cantidad, mejores composiciones).
- Además, un **ciclo lunar** visible en el HUD modula la intensidad:
  - **Luna nueva → creciente:** noches estándar.
  - **Luna llena:** los aliens canalizan la energía lunar y llegan **transformados/potenciados** (concepto hombre-lobo, sin lobos): más fuertes, variantes especiales, posible mini-jefe.
- La luna llena funciona como el "examen" periódico del run: telegrafiada con días de anticipación, fuerza a preparar defensas para picos, no solo para el goteo nocturno.
- **El respiro post-luna-llena (decidido, §13.1 D4).** Después de cada luna llena, las **2–3 noches siguientes son más suaves** — menos intensidad de oleada— para que el rancho se recupere del pico. La referencia declarada es *Kingdom*: pico, respiro, pico más alto. Es la única forma de piedad que tiene el juego, y no toca la progresión: **no relaja ninguna compuerta de la curva del científico** (§6.4), baja la presión de las noches. La razón es que el robo castiga en espiral (§5.3), y una espiral sin valle no se sale nunca: el respiro es el tramo donde se puede revertir **jugando**. Cuántas noches exactas y cuánto baja la intensidad son `TBD` ([`WIKI.md §8.2`](WIKI.md#82-el-respiro-post-luna-llena--la-piedad-decidida-por-mato)).
- **Por definir:** duración del ciclo (¿cada 6–8 noches?) y si la luna llena coincide con hitos del escalado.

---

## 10. Enemigos (Wiki — taxonomía v0.1)

> ⚠️ **Fuente canónica: [`WIKI.md`](WIKI.md#2-enemigos)** ([índice](wiki/README.md#enemigos)). Aquí solo la taxonomía y la regla de diseño; fichas completas en la wiki.

> Regla de oro: **cada enemigo quiere llevarse algo.** Su diseño responde a: ¿qué roba, cómo lo roba y cómo lo evitas?

> **Cambio v0.4 — a quién le roban.** Ya no hay muro que cruzar: el alien va al **edificio-refugio más cercano** que tenga lo que busca y **tarda en sacarlo** (1–3 s por persona, 2 s por recurso, ganado `TBD`). Durante esa ventana está quieto y expuesto (§6.3). Consecuencia sobre la taxonomía: los **tanques**, que existían para romper muros, pasan a atacar **torres y edificios**; y tres fichas canon diseñadas contra barricadas (*Manos Largas*, *Toro de Marte*, *El Ganadero*) volvieron a `propuesta` en la wiki hasta validar su nuevo mecanismo.

### 10.1 Categoría: LADRONES (rateros rápidos)
*Roban recursos sueltos y objetos. Frágiles, veloces, vienen en grupo. Entran, agarran y huyen.*

| Enemigo | Comportamiento | Contramedida |
|---|---|---|
| **Ratero Gris** | Alien pequeño; corre al depósito más cercano, toma lo que puede y huye por donde vino | Cualquier defensa; el problema es el volumen |
| **Coyote Plateado** | Bestia alienizada; muy rápido, esquiva en zigzag; prioriza comida | Escopetas / trampas |
| **Manos Largas** | Brazos elásticos: roba **desde afuera del refugio**, por la ventana, sin cruzar la puerta — los defensores de adentro no lo alcanzan (con muros opcionales activos, roba además por encima de las barricadas bajas) | Eliminarlo a distancia, o una torre en prioridad *"el que ya carga"* |

### 10.2 Categoría: ABDUCTORES (se llevan lo vivo)
*El corazón del hook. Voladores con rayo tractor. Si derribas la nave a tiempo, la víctima cae y se salva.*

| Enemigo | Comportamiento | Contramedida |
|---|---|---|
| **Platillo Sonda** | Pequeño OVNI; rayo tractor lento sobre ganado | DPS aéreo básico; da tiempo de reacción |
| **Platillo Abductor** | Versión mayor; rapta **personas**; escudo frontal débil por detrás | Cazadores / arpón antigravedad |
| **Sombrero Negro** | Alien terrestre con disfraz de forastero; se infiltra de noche y "se lleva caminando" a un aldeano hipnotizado | Torre de vigilancia lo revela; tensión de detección |

### 10.3 Categoría: TANQUES (abren camino)
*No roban: rompen. Sin muros que derribar, su blanco pasa a ser lo que sí estorba — **torres y edificios-refugio**. Reventar un refugio no destruye lo de adentro: lo deja al descubierto y acelera el saqueo de los demás.*

| Enemigo | Comportamiento | Contramedida |
|---|---|---|
| **Toro de Marte** | Cuadrúpedo masivo; embiste torres y las puertas de los refugios; telegrafiada su carga | Daño concentrado, dinamita |
| **Caparazón** | Lento, blindaje frontal total; absorbe el fuego de las torres mientras los ladrones saquean detrás | Flanqueo, daño en área, plasma (ignora armadura) |
| **Demoledor** | Lanza proyectiles de asedio contra torres desde media distancia | Salir a cazarlo o fuego de largo alcance |

### 10.4 Categoría: SOPORTE (los "magos")
*No roban ni rompen: potencian a los demás. Prioridad de fuego alta.*

| Enemigo | Comportamiento | Contramedida |
|---|---|---|
| **Psíquico Velado** | Proyecta escudos sobre otros aliens | Matarlo primero; el pánico de verlo llegar |
| **Reparador** | Dron que cura/repara tanques y naves | Cazadores |
| **Hipnotizador** | Voltea temporalmente a una unidad tuya (pelea en tu contra; no puede ser raptada mientras) | Romper el canal dañándolo |
| **Faro Lunar** | Solo en luna llena: amplifica la transformación lunar de los cercanos | Objetivo prioritario del "examen" lunar |

### 10.5 Categoría: JEFES
| Enemigo | Comportamiento |
|---|---|
| **Nave Capataz** | Mini-jefe de luna llena; combina rayo tractor masivo + escolta |
| **El Ganadero** | Jefe mid-game; alien colosal que "cosecha" — arranca del suelo las torres colocadas (y las barricadas, si la variante clásica está activa) y las usa de arma |
| **Nave Nodriza** | Objetivo final. No ataca tu pueblo: la asaltas tú, de día, con tu milicia armada con tec alien. Fases: escudo → torretas → núcleo |

### 10.6 Reglas de comportamiento comunes
- Al **amanecer**, todo alien vivo huye llevándose lo que cargue.
- Todo alien puede soltar **componentes** al morir (más raros según categoría).
- Composición de oleadas = presupuesto de puntos por noche × modificador lunar (sistema estándar TD, a detallar en doc de balance).

---

## 11. Condiciones de Fin

- **Derrota:** los aliens arrasan el pueblo en una noche (población/defensa insuficiente por la espiral de robos). No hay objeto-corona.
- **Victoria:** destruir la Nave Nodriza mediante el asalto diurno.
- En ambos casos → pantalla de resumen del run → puntos de meta-progresión.

---

## 12. Arte, Tono y Ambientación

- **Pixel art**, referencias: Kingdom (siluetas, iluminación, atmósfera) + expresividad cómica.
- **Tono:** cómic pulp de los 50s aplicado al Weird West — gracioso en la superficie, inquietante en la incertidumbre. Las vacas flotando en rayos tractores son cómicas; el bosque de noche y el silencio antes de la luna llena, no.
- **Época:** 1870s clásico + Weird West (tecnología imposible, ciencia de feria, elixires).
- **Audio:** guitarra/armónica de western contaminándose progresivamente con theremín y sintetizadores según avanza la invasión (idea a explorar).

---

## 13. Preguntas Abiertas (para v0.5)

### 13.1 Decisiones del diseño defensivo — cerradas por Mato

> Salieron del cambio de mecánica de v0.4. **Mato cerró las seis el 29 de agosto
> de 2026**: cinco con una respuesta directa y la sexta (D4) pasando por una fase
> de balance que él mismo pidió y aprobó el mismo día. El registro canónico —con
> el detalle de cada una y las fichas que toca— está en
> [`WIKI.md §9`](WIKI.md#9-decisiones-registradas-y-lo-que-sigue-abierto);
> esto es el resumen.

**Resueltas (29 de agosto de 2026)**

- ✅ **D1 — Variante A: los aliens atacan las torres primero.** No las ignoran ni es configurable: el alien resuelve la torre que lo engancha antes de seguir al refugio, así que colocar una torre es elegir *dónde se pelea* (§6.3)
- ✅ **D2 — No hay muros, ni siquiera como variante.** El rancho queda abierto: la defensa es refugio + torres. `barricada` se archiva y los tres enemigos diseñados contra ella se rediseñan (`TASK-020`) (§6.1, §6.3)
- ✅ **D3 — 3–5 s por cosa robada, aleatorio**, sea aldeano, comida o vaca; los aliens grandes se llevan **dos** cosas y tardan más (multiplicador pendiente de balance). Revisa el 1–3 s / 2 s de v0.4 (§6.3)
- ✅ **D4 — La curva de progresión del científico, aprobada.** No fue un número elegido a ciegas: pasó por una fase de balance (`TASK-021`), el equipo propuso la forma y Mato la aprobó en tres puntos — **cuatro compuertas** sobre tres ejes (sobrevivencia, comunidad, capacidad económica) con el científico al final; el **`doctor` se desbloquea en la segunda compuerta**, *"para que pueda sobrevivir hasta el final"*; y la piedad va **ON en una forma concreta**: tras la luna llena, **2–3 noches suaves** para recuperarse, *"como Kingdom"* (§6.4, §9). **Lo aprobado es la forma: los parámetros siguen `TBD`** y se calibran en el prototipo
- ✅ **D5 — El campo de fuerza es una estructura, y un desbloqueo post-científico.** Las mejoras se pagan en **piezas alien**, recogidas de mañana en el **barrido del amanecer** sobre las naves caídas (§8.1)
- ✅ **D6 — Árbol de talentos por edificio**, que se abre clickeando ese edificio: lo que comprás no vale ni para otro edificio del mismo tipo. No hay árbol global; la progresión *es* el layout (§6.5)

**Lo que sigue abierto**

**Nada.** Las seis decisiones del cambio de mecánica están cerradas. Lo que
queda de D4 no es una decisión sino **calibración numérica**: los parámetros de
la curva (`P1_vacas`, `P4_vacas`, `N_objetivo`, el respiro…) se fijan con el
juego andando (`TASK-010` / `TASK-005`), no en la mesa. Tabla de parámetros en
[`WIKI.md §9.2`](WIKI.md#92-d4--la-forma-está-aprobada-los-números-son-del-prototipo).

### 13.2 Preguntas de fondo (venían de v0.3)
1. Lista final de edificios y sus árboles de mejora. (§6.2, §6.5)
2. ¿Armas alien = clase nueva o mejora de equipo? (§7)
3. Nombre y tamaño del sistema de meta-progresión. (§8.3) — *el **eje** ya está decidido: las tres clases del héroe (§4.3). Falta el nombre de los puntos, el tamaño del árbol y cuántos héroes por clase*
4. Duración exacta del ciclo lunar y curvas de dificultad. (§9) — *el **respiro post-luna-llena** ya está decidido (§13.1 D4): 2–3 noches suaves después de cada llena. Falta el largo del ciclo y cuánto baja la intensidad*
5. Economía: ¿confirmamos la ausencia de oro tras el primer prototipo?
6. Nombre definitivo del juego.

### Resueltas tras v0.4 (29 de agosto de 2026)
- ✅ **El héroe tiene clase:** Sheriff (ataque), Alcalde (economía), Carpintero (defensa y capacidad) — una clase = un eje, se elige al empezar la run (§4.3)
- ✅ **El meta-juego cuelga de las clases:** los puntos de fin de run mejoran tu héroe o desbloquean héroes nuevos dentro de esas tres clases (§8.3)

### Resueltas en v0.4
- ✅ **Sin muros por defecto:** el rancho está abierto; la defensa son edificios-refugio + torres colocables (§6.1, §6.3)
- ✅ **Los edificios tienen dos vidas:** función económica de día, refugio o defensa de noche (§6.2)
- ✅ **El robo lleva tiempo y esa ventana es el juego:** matarlo cargado le hace soltar el botín (§6.3). *El 1–3 s / 2 s de v0.4 quedó revisado por D3: hoy son 3–5 s para todo*
- ✅ **Torres colocables libremente y configurables** por prioridad de objetivo (§6.3)
- ✅ **El ganado come:** cadena pasto → vaca → comida, con hambre si el rebaño crece más rápido que las granjas (§5.4)
- ✅ **Los edificios suben de nivel** por una de dos ramas excluyentes: refugio+defensa o doble refugio (§6.5)
- ✅ **Hay desbloqueos por objetivos:** el científico llega por criar ganado, no por renombre difuso (§6.4)
- ✅ **La barrera alien es el "muro" del late game**, y llega tarde a propósito (§8.1)

### Resueltas en v0.3
- ✅ Split screen dinámico: se une cuando los jugadores están cerca (§4.2)
- ✅ Fuera de combate: revives Malherido al amanecer donde caíste y regresas al pueblo; sin penalización extra (§4.1, §4.2)
- ✅ Wiki de unidades y enemigos separada a [`WIKI.md`](WIKI.md) como fuente canónica; §7 y §10 de este documento pasan a ser resumen de diseño

### Resueltas en v0.2
- ✅ Derribo del héroe → sistema de 3 estados (§4.1)
- ✅ Mapa → fijo con fondo/recursos semi-aleatorios; pueblos/ciudades como progresión futura (§3.4)
- ✅ Coop → local 2P split screen desde el diseño inicial; sin online (§4.2)

---

## 14. Roadmap Sugerido
1. **Prototipo de core loop (4–6 semanas):** ciclo día/noche, 1 recurso, peones, 2 enemigos (Ratero + Platillo Sonda con rayo tractor y drop de víctima), **un edificio-refugio con ventana de robo y una torre colocable con prioridad de objetivo**, **arquitectura preparada para 2 héroes** (aunque el coop se pruebe en fase 2). **Meta: validar que "el robo duele" se siente** — y que la ventana de robo se lee sin explicación.
2. **Vertical slice:** economía completa (incluida la cadena pasto → vaca → comida), 5–6 enemigos, árbol tec T1→T2, niveles de edificio, primera luna llena.
3. **Loop de run completo:** derrota por espiral, asalto a nodriza, meta-progresión mínima.
4. **Contenido y balance:** wiki completa de enemigos/unidades, T3, jefes.

---

## Anexo A — Selección de Motor

| Criterio | Godot 4 | Unity 2D | Phaser |
|---|---|---|---|
| Costo | Gratis, MIT, sin regalías | Gratis <200K USD/año; Pro de pago | Gratis |
| Pipeline 2D / pixel art | Nativo, pixel-perfect de fábrica | Sobre motor 3D; requiere configuración | Bueno, pero orientado a web |
| Lenguaje | GDScript / **C#** | C# (experiencia actual del equipo) | JavaScript/TS |
| Consolas | Vía terceros (W4 Games) | Soporte oficial | No viable |
| Peso de builds | Muy liviano | Pesado para 2D | N/A escritorio |
| Ecosistema/assets | Creciente | El más grande | Limitado para este alcance |
| Amigable a workflows agénicos | Alta (proyectos en texto plano, open source) | Media | Alta |

**Recomendación: Godot 4 con C#.** Aprovecha la experiencia en C#, costo cero, 2D nativo ideal para pixel art. Unity queda como plan B legítimo si la rampa de aprendizaje resultara un problema en el prototipo. Phaser descartado (web-first, sin camino real a consola).

---

*Documento vivo. Siguiente iteración: v0.5 con las seis decisiones de §13.1 cerradas —incluida la curva de progresión de D4, aprobada en su forma— y el prototipo del core loop validado, que es de donde salen los números que siguen `TBD`.*
