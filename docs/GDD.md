# COWBOY DEFENSE — Game Design Document v0.3

> **Estado:** Tercer borrador · **Fecha:** Agosto 2026 · **Equipo:** 2 personas + sistemas agénicos
> **Documentos hermanos:** [`WIKI.md`](WIKI.md) (fuente canónica de unidades y enemigos) · [`TECH.md`](TECH.md) (documento técnico) · [índice navegable de la wiki](wiki/README.md)
> **Nombre tentativo:** Cowboy Defense (working title)

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
```

- **Día (duración fija):** los trabajadores recolectan en el rango cercano al pueblo; el jugador cabalga a explorar más lejos, encuentra recursos, sitios de interés y reclutas.
- **Noche (duración fija):** oleadas de aliens entran por **izquierda y derecha**; más adelante, **naves por arriba**. Torres y unidades pelean solas. El jugador reposiciona, gasta recursos de emergencia y los reparadores mantienen barricadas.
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

---

## 5. Recursos y Economía

### 5.1 Recursos (sin oro — decisión tentativa)
| Recurso | Fuente | Uso | Robable |
|---|---|---|---|
| **Madera** | Árboles del entorno (taladores) | Construcción y expansión de barricadas/edificios | Sí |
| **Chatarra / Tec. alienígena** | Restos de aliens y naves derribadas, sitios de crash, hallazgos del desierto | Investigación, armas, torres avanzadas, mejoras | Sí |
| **Comida** | Ganado (pasivo), caza, cultivos | Mantiene a la población. Sin comida → la gente muere/deserta en ~2 días | Sí (¡y el ganado también!) |
| **Población** | Reclutas encontrados/atraídos | Es el recurso vivo: trabajan, pelean, investigan | **Sí — es lo que más roban** |

- Chatarra y tecnología alien son **el mismo recurso**: recoges tec alien y la refinas/mejoras.
- Nota de diseño: si en prototipo la economía pide una moneda blanda universal, se reevalúa el oro.

### 5.2 Transporte físico de recursos
- Los recursos **existen físicamente**: aparecen en el mundo, un trabajador los carga y los deposita en el almacén/edificio correspondiente.
- Consecuencia clave: los recursos en tránsito son vulnerables. Si un abductor se lleva una vaca y **derribas la nave a tiempo, la vaca cae viva** y la recuperas. Si la nave sale de pantalla / termina la noche: **se perdió para siempre.** No hay rescate posterior.

### 5.3 La espiral del robo (mecánica central)
- Te roban vacas → mañana produces menos comida → alimentas menos gente → menos defensores → la próxima noche te roban más.
- El día siguiente a una mala noche es de **recuperación**: decidir si reponer comida, reponer gente o reforzar defensa es el corazón estratégico del juego.

---

## 6. El Rancho (Base)

### 6.1 Layout
- **Layout fijo con slots de mejora.** Centro: **Town Center**. A los lados, slots de edificios; en los bordes, líneas de defensa.
- El territorio se puede **expandir** (como Kingdom): empujar las barricadas hacia afuera abarca más slots, más recursos… y más frente que defender.

### 6.2 Edificios (propuesta inicial — por definir en detalle)
| Edificio | Función |
|---|---|
| **Town Center** | Núcleo. Almacén principal. Nivel del pueblo = desbloqueos |
| **Taberna / Inn** | Atrae y aloja reclutas; asignación de roles |
| **Establo / Corral** | Aloja ganado; produce comida pasiva; mejorable (más vacas, vacas protegidas) |
| **Armería / Herrería** | Fabrica y mejora armas humanas; equipa unidades |
| **Laboratorio del Profesor** | Llega con científicos (§7); investiga tecnología alien; árbol tecnológico |
| **Torre de vigilancia** | Slot de torre defensiva; recibe las armas del árbol tec |
| **Granja** | Comida activa (cultivos), complementa al ganado |
| **Barricadas / Muros** | Línea defensiva por niveles (madera → reforzada → tec alien) |

### 6.3 Defensa y reparación
- Muros y torres se construyen/mejoran **también durante la noche** si hay recursos y manos.
- **Reparación activa estilo RTS:** un trabajador puede reparar una barricada *mientras* recibe daño (riesgo: el reparador es raptable).
- Ataques por ambos flancos obligan a repartir defensa; las naves aéreas (mid-game) obligan a tener antiaéreo.

---

## 7. Unidades del Jugador (Wiki — propuesta inicial)

> ⚠️ **Fuente canónica: [`WIKI.md`](WIKI.md#1-unidades-del-jugador)** ([índice](wiki/README.md#unidades-del-jugador)). Las tablas de este documento son el resumen de diseño; las fichas completas, stats y drops viven en la wiki.

> Todas las unidades son **raptables**. Perder una unidad no es solo perder DPS: es perder su función económica.

| Unidad | Rol | Cómo se obtiene | Notas |
|---|---|---|---|
| **Peón** | Recolecta madera/chatarra, construye, repara | Recluta base (Taberna) | La sangre del pueblo. Objetivo favorito de los Ladrones |
| **Pistolero** | Defensa básica a distancia | Peón + revólver (Armería) | Evoluciona con armas del árbol tec |
| **Cazador** | Genera comida de día; francotirador de noche | Peón + rifle | Largo alcance, cadencia lenta. Bueno contra voladores |
| **Chatarrero (Scavenger)** | Especialista en recoger tec alien del campo y de la batalla | Peón + mejora en Laboratorio | Recoge más rápido y más lejos; clave para el árbol tec |
| **Vaquero de ganado** | Pastorea y protege el ganado; lazo | Peón + Establo | Puede **enlazar** aliens pequeños o jalar de vuelta ganado abducido (a validar) |
| **Científico / Profesor** | Investiga tecnología alien; desbloquea armas | Llega al pueblo al alcanzar cierto nivel/renombre (o se encuentra explorando) | No pelea. Si te lo raptan, la investigación se detiene |
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
  - **T3 Alien:** rifle de plasma, torre de rayo, bomba de gas lumínico, barrera de energía, arpón antigravedad (baja naves).

### 8.2 Captura de tecnología, no de aliens
- **No hay captura de aliens vivos** (descartado). Toda la tec viene de restos y sitios de crash.

### 8.3 Meta-progresión (entre runs)
- Al final de cada run (victoria o derrota) ganas **puntos** según noches sobrevividas, tec investigada, jefes derrotados, gente salvada.
- Se gastan en mejoras permanentes tipo roguelike: tecnologías pre-desbloqueadas, +daño del héroe, empezar con una unidad extra, descuentos, nuevos edificios disponibles, etc.
- **Por definir:** nombre/ficción de estos puntos (¿"Renombre"? ¿"Recortes de periódico"?) y el tamaño del árbol meta.

---

## 9. Escalada de Dificultad — El Ciclo Lunar

- La dificultad escala **por noche** (más cantidad, mejores composiciones).
- Además, un **ciclo lunar** visible en el HUD modula la intensidad:
  - **Luna nueva → creciente:** noches estándar.
  - **Luna llena:** los aliens canalizan la energía lunar y llegan **transformados/potenciados** (concepto hombre-lobo, sin lobos): más fuertes, variantes especiales, posible mini-jefe.
- La luna llena funciona como el "examen" periódico del run: telegrafiada con días de anticipación, fuerza a preparar defensas para picos, no solo para el goteo nocturno.
- **Por definir:** duración del ciclo (¿cada 6–8 noches?) y si la luna llena coincide con hitos del escalado.

---

## 10. Enemigos (Wiki — taxonomía v0.1)

> ⚠️ **Fuente canónica: [`WIKI.md`](WIKI.md#2-enemigos)** ([índice](wiki/README.md#enemigos)). Aquí solo la taxonomía y la regla de diseño; fichas completas en la wiki.

> Regla de oro: **cada enemigo quiere llevarse algo.** Su diseño responde a: ¿qué roba, cómo lo roba y cómo lo evitas?

### 10.1 Categoría: LADRONES (rateros rápidos)
*Roban recursos sueltos y objetos. Frágiles, veloces, vienen en grupo. Entran, agarran y huyen.*

| Enemigo | Comportamiento | Contramedida |
|---|---|---|
| **Ratero Gris** | Alien pequeño; corre al depósito más cercano, toma lo que puede y huye por donde vino | Cualquier defensa; el problema es el volumen |
| **Coyote Plateado** | Bestia alienizada; muy rápido, esquiva en zigzag; prioriza comida | Escopetas / trampas |
| **Manos Largas** | Brazos elásticos: roba **por encima** de barricadas bajas sin romperlas | Muros altos o eliminarlo a distancia |

### 10.2 Categoría: ABDUCTORES (se llevan lo vivo)
*El corazón del hook. Voladores con rayo tractor. Si derribas la nave a tiempo, la víctima cae y se salva.*

| Enemigo | Comportamiento | Contramedida |
|---|---|---|
| **Platillo Sonda** | Pequeño OVNI; rayo tractor lento sobre ganado | DPS aéreo básico; da tiempo de reacción |
| **Platillo Abductor** | Versión mayor; rapta **personas**; escudo frontal débil por detrás | Cazadores / arpón antigravedad |
| **Sombrero Negro** | Alien terrestre con disfraz de forastero; se infiltra de noche y "se lleva caminando" a un aldeano hipnotizado | Torre de vigilancia lo revela; tensión de detección |

### 10.3 Categoría: TANQUES (abren camino)
*No roban: rompen. Existen para destruir barricadas y dejar pasar a los demás.*

| Enemigo | Comportamiento | Contramedida |
|---|---|---|
| **Toro de Marte** | Cuadrúpedo masivo; embiste muros; telegrafiada su carga | Daño concentrado, dinamita |
| **Caparazón** | Lento, blindaje frontal total | Flanqueo, daño en área, plasma (ignora armadura) |
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
| **El Ganadero** | Jefe mid-game; alien colosal que "cosecha" — arranca barricadas y las usa de arma |
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

## 13. Preguntas Ab