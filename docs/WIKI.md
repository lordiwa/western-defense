# COWBOY DEFENSE — Wiki de Entidades v0.2

> **Propósito:** Fuente canónica de todas las entidades del juego (unidades del jugador, enemigos, armas, edificios, oleadas). Este documento está estructurado para ser **consumido por sistemas de IA** que generen la wiki pública, assets, código de datos (ScriptableObjects / Resources) o contenido de balance.
> **Documentos hermanos:** [`GDD.md`](GDD.md) (diseño general) · [`TECH.md`](TECH.md) (técnico)
> **Navegación:** [índice de la wiki](wiki/README.md) — tablas por categoría con enlaces a cada ficha (generado, no editar a mano).

> ### ⚠️ v0.2 — cambio de mecánica del núcleo defensivo
> El equipo decidió (agosto 2026) que **el rancho no tiene muros por defecto**: la
> invasión es sorpresa, todo está abierto y los aliens bajan de sus naves. La
> defensa pasa a ser **edificios-refugio + torres colocables**, y el robo deja de
> ser "pasar el muro" para ser "entrar al refugio y tardar en sacar lo que hay"
> ([§5.0](#50-reglas-de-los-edificios-de-noche-cambio-canónico)).
> Las **decisiones que siguen abiertas** — y que nadie resuelve por su cuenta —
> están en [§9](#9-decisiones-abiertas-para-el-equipo). Resumen de diseño en
> [GDD §6](GDD.md#6-el-rancho-base).

---

## 0. Instrucciones para sistemas de IA

Si eres una IA procesando este documento:

1. Cada entidad es una **ficha** con esquema fijo. Los campos con valor `TBD` están pendientes de balance — no los inventes salvo que se te pida explícitamente proponer valores.
2. El campo `id` es el identificador canónico (snake_case, estable): úsalo para nombres de archivo, clases, claves de datos y referencias cruzadas.
3. Las categorías de enemigos (`ladron`, `abductor`, `tanque`, `soporte`, `jefe`) definen comportamiento base heredable; la ficha solo describe lo que difiere.
4. La regla de diseño de todo enemigo: **quiere llevarse algo**. Si generas enemigos nuevos, deben responder: ¿qué roba, cómo lo roba, cómo se evita?
5. Tono del universo: Weird West 1870s, cómic pulp — gracioso en la superficie, inquietante en la incertidumbre. Sin gore.
6. Al generar contenido nuevo, mantén los campos del esquema y marca la ficha con `estado: propuesta`.

### Esquema de ficha — Unidad del jugador
```yaml
id:            # snake_case canónico
nombre:        # nombre en español
tipo: unidad_jugador
rol:           # economico | defensivo | mixto | investigacion
obtencion:     # cómo se consigue
desbloqueo_objetivo: # id del objetivo de §8 que la habilita; `n/a` si no aplica
funcion_dia:   # qué hace durante el día
funcion_noche: # qué hace durante la noche
arma_base:     # arma inicial si aplica
raptable: true # todas las unidades lo son
stats: {vida: TBD, dano: TBD, cadencia: TBD, rango: TBD, velocidad: TBD}
costo: {madera: TBD, chatarra: TBD, comida_upkeep: TBD}
mejoras:       # lista de mejoras posibles
notas_diseno:  # intención de diseño
estado:        # canon | propuesta
```

### Esquema de ficha — Enemigo
```yaml
id:
nombre:
tipo: enemigo
categoria:     # ladron | abductor | tanque | soporte | jefe
que_roba:      # recursos | ganado | personas | nada (rompe) | nada (potencia)
como_roba:     # descripción del mecanismo
contramedida:  # cómo lo evita el jugador
movimiento:    # terrestre | volador
aparicion:     # rango de noches / condición (ej. solo luna llena)
tiempo_robo:   # cuánto tarda por víctima dentro del refugio. `default` hereda
               # los tiempos de la oleada (§5.0); un valor propio lo sobreescribe.
               # El tiempo del ganado sigue sin decidir (§9, D3).
stats: {vida: TBD, dano: TBD, velocidad: TBD, capacidad_robo: TBD}
drops:         # componentes que suelta al morir + rareza
comportamiento_amanecer: huye con lo que cargue  # default
notas_diseno:
estado:
```

### Esquema de ficha — Arma
```yaml
id:            # snake_case canónico
nombre:        # nombre en español
tipo: arma
tier:          # T1_humano | T2_hibrido | T3_alien (GDD §8.1)
montaje:       # unidad | torre | trampa — quién o qué la lleva
fabricacion:   # dónde y con qué se consigue (edificio + requisito de investigación)
efecto:        # qué hace en combate
stats: {dano: TBD, cadencia: TBD, rango: TBD, area: TBD}
costo: {madera: TBD, chatarra: TBD, componentes: TBD}
mejoras:       # lista de mejoras posibles
notas_diseno:  # intención de diseño
estado:        # canon | propuesta
```
> Los `stats` del arma están todos en `TBD`: hoy los valores cualitativos que existen viven en la ficha de la unidad que la porta (`pistolero.stats.rango`, etc.). Qué lado manda cuando haya números es una decisión de balance pendiente.

### Esquema de ficha — Edificio
```yaml
id:            # snake_case canónico
nombre:        # nombre en español
tipo: edificio
funcion:       # resumen de para qué sirve (GDD §6.2)
funcion_dia:   # qué hace mientras hay luz
funcion_noche: # en qué se convierte al caer la noche (ver modo_noche)
modo_noche:    # refugio | defensa | refugio_y_defensa | ninguno — regla de §5.0
capacidad_refugio: # cuánta gente y cuántos recursos resguarda de noche (TBD hasta balance)
prioridad_objetivo: # solo si modo_noche incluye defensa: primero_en_llegar |
               # mas_cercano_a_recursos | ya_cargado (§5.0). `n/a` si no dispara.
slot:          # centro | lateral | linea_defensa | libre (colocable donde el
               # jugador quiera, GDD §6.1)
obtencion:     # cómo se habilita o se construye
desbloquea:    # SOLO ids de esta wiki, en lista. Si lo que habilita todavía no
               # es una ficha, va `TBD`; si no habilita entidades, va `n/a`.
               # Lo que quede fuera se explica en `notas_diseno`. Esta lista es
               # verificable por referencia cruzada (TASK-009): nada de prosa.
niveles:       # progresión de mejora del edificio. Las dos ramas canónicas de
               # §5.0 son refugio_y_defensa y doble_refugio; se desbloquean por
               # árbol de habilidades + tecnología alien.
stats: {vida: TBD, tiempo_construccion: TBD}
costo: {madera: TBD, chatarra: TBD}
notas_diseno:  # intención de diseño
estado:        # canon | propuesta
```
> Los campos `funcion_dia`, `funcion_noche`, `modo_noche`, `capacidad_refugio` y
> `prioridad_objetivo` entraron con el cambio de mecánica de defensa (§5.0). El
> edificio dejó de ser decorado económico: de noche **es** la defensa.

### Esquema de ficha — Recurso
```yaml
id:            # snake_case canónico
nombre:        # nombre en español
tipo: recurso
clase:         # vivo | consumible | materia_prima
fuente:        # de dónde sale (edificio, entorno, evento)
consumo:       # quién lo consume y con qué ritmo
robable:       # si | no — y por quién
funcion_dia:   # qué pasa con él mientras hay luz
funcion_noche: # qué pasa con él de noche (se guarda, queda expuesto, se sigue consumiendo)
stats: {produccion: TBD, consumo_por_unidad: TBD, capacidad: TBD}
notas_diseno:  # intención de diseño
estado:        # canon | propuesta
```
> Tipo nuevo: existe porque el ganado dejó de ser "comida pasiva" para volverse
> una cadena (pasto → vaca → comida) con puntos de fallo propios (§7).

### Esquema de ficha — Oleada
```yaml
id:                # snake_case canónico
nombre:            # nombre en español
tipo: oleada
noche:             # noche o rango de noches al que aplica
fase_lunar:        # cualquiera | nueva | creciente | llena | menguante (GDD §9)
presupuesto:       # puntos de la noche antes del modificador (TECH §3.3)
modificador_lunar: # multiplicador del presupuesto según la fase
enemigos:          # qué enemigos son elegibles esa noche
spawn: {flancos: TBD, paths_voladores: TBD}
tiempos_robo: {persona_s: 1-3, recurso_s: 2}  # cuánto tarda un alien dentro de
                   # un edificio por cada víctima (§5.0). El valor por persona
                   # se sortea dentro del rango una vez por oleada.
determinista: true # la composición se resuelve con el seed del run (TECH §3.3)
notas_diseno:      # intención de diseño
estado:            # canon | propuesta
```
> El **costo en puntos de cada enemigo** no vive acá: es un campo de la ficha de enemigo, todavía sin definir (ver el backlog de §10). La oleada solo aporta el presupuesto y el marco de spawn.

---

## 1. Unidades del Jugador

### 1.1 peon
```yaml
id: peon
nombre: Peón
tipo: unidad_jugador
rol: economico
obtencion: Recluta base en la Taberna
desbloqueo_objetivo: n/a
funcion_dia: Recolecta madera y chatarra, construye edificios
funcion_noche: Se refugia en el edificio-refugio asignado; puede salir a reparar torres y edificios bajo fuego (riesgo de rapto)
arma_base: ninguna
raptable: true
stats: {vida: TBD, dano: 0, cadencia: n/a, rango: n/a, velocidad: TBD}
costo: {madera: 0, chatarra: 0, comida_upkeep: TBD}
mejoras: [carretilla (más carga), herramientas (construye más rápido)]
notas_diseno: La sangre del pueblo y el objetivo favorito de los Ladrones. Su pérdida frena toda la economía. Desde v0.2 el peón de noche no defiende un muro sino que ES el botín que hay dentro del refugio — sacarlo de ahí lleva 1-3 s al alien (§5.0), y esa ventana es lo que tus torres aprovechan.
estado: canon
```

### 1.2 pistolero
```yaml
id: pistolero
nombre: Pistolero
tipo: unidad_jugador
rol: defensivo
obtencion: Peón + revólver fabricado en la Armería
desbloqueo_objetivo: n/a
funcion_dia: Escolta a recolectores fuera del rancho
funcion_noche: Defensa a distancia; se posiciona entre los edificios-refugio y tira sobre los aliens que están saqueando
arma_base: revolver
raptable: true
stats: {vida: TBD, dano: TBD, cadencia: TBD, rango: medio, velocidad: TBD}
costo: {madera: 0, chatarra: TBD, comida_upkeep: TBD}
mejoras: [equipo del árbol tecnológico (T1 rifle → T2 híbrido → T3 plasma)]
notas_diseno: Las armas alien NO crean clases nuevas; son mejoras de equipo sobre esta unidad (pendiente de confirmar, ver GDD §13).
estado: canon
```

### 1.3 cazador
```yaml
id: cazador
nombre: Cazador
tipo: unidad_jugador
rol: mixto
obtencion: Peón + rifle largo
funcion_dia: Caza animales → genera comida
funcion_noche: Francotirador de largo alcance; prioriza voladores
arma_base: rifle_largo
raptable: true
stats: {vida: TBD, dano: alto, cadencia: lenta, rango: largo, velocidad: TBD}
costo: {madera: 0, chatarra: TBD, comida_upkeep: TBD}
mejoras: [mira (más rango), munición perforante]
notas_diseno: Doble función comida/antiaéreo. Raptarlo duele por dos lados.
estado: canon
```

### 1.4 chatarrero
```yaml
id: chatarrero
nombre: Chatarrero (Scavenger)
tipo: unidad_jugador
rol: economico
obtencion: Peón + mejora en el Laboratorio
funcion_dia: Recoge tecnología alien del campo y de sitios de crash, más rápido y más lejos que un peón
funcion_noche: Recoge drops durante la batalla (alto riesgo)
arma_base: ninguna
raptable: true
stats: {vida: TBD, dano: 0, cadencia: n/a, rango: n/a, velocidad: alta}
costo: {madera: 0, chatarra: TBD, comida_upkeep: TBD}
mejoras: [saco antigrav (más carga), botas (más velocidad)]
notas_diseno: Motor del árbol tecnológico. Recoger drops en plena noche es la apuesta riesgo/recompensa de la unidad.
estado: canon
```

### 1.5 vaquero_ganado
```yaml
id: vaquero_ganado
nombre: Vaquero de ganado
tipo: unidad_jugador
rol: mixto
obtencion: Peón + Establo construido
desbloqueo_objetivo: n/a
funcion_dia: Lleva las vacas al pasto que crece alrededor de la granja y el establo (§7) y aumenta la producción de comida; cuantas más vacas maneje, más rápido se consume el pasto
funcion_noche: Al atardecer guarda las vacas dentro del establo y espera la invasión ahí; protege el corral y puede enlazar con lazo
arma_base: lazo
raptable: true
stats: {vida: TBD, dano: bajo, cadencia: TBD, rango: corto, velocidad: TBD}
costo: {madera: 0, chatarra: TBD, comida_upkeep: TBD}
mejoras: [lazo reforzado]
notas_diseno: Mecánica a validar en prototipo — el lazo puede jalar de vuelta ganado siendo abducido o inmovilizar aliens pequeños. Con el pastoreo de v0.2 su trabajo diurno pasa a ser una decisión real: más vacas al pasto es más comida hoy y menos pasto mañana (§7).
estado: propuesta
```

### 1.6 cientifico
```yaml
id: cientifico
nombre: Científico / Profesor
tipo: unidad_jugador
rol: investigacion
obtencion: Objetivo de desbloqueo — llega al pueblo cuando el rancho sostiene X vacas vivas (§8, objetivo_cientifico). También puede encontrarse explorando
desbloqueo_objetivo: objetivo_cientifico
funcion_dia: Investiga tecnología alien en el Laboratorio; desbloquea recetas del árbol tecnológico
funcion_noche: Se refugia (no pelea)
arma_base: ninguna
raptable: true
stats: {vida: baja, dano: 0, cadencia: n/a, rango: n/a, velocidad: baja}
costo: {madera: 0, chatarra: 0, comida_upkeep: TBD}
mejoras: [asistente (segunda cola de investigación)]
notas_diseno: Si te lo raptan, la investigación se DETIENE. Es la unidad más valiosa y más frágil — protegerlo es una decisión de layout. Desde v0.2 su llegada es un OBJETIVO explícito y no un umbral difuso de renombre — el ranchero que junta vacas se gana al científico, que es la manera del juego de decir "criar ganado también es progresión tecnológica". El número de vacas es TBD (§9, D4).
estado: canon
```

### 1.7 dinamitero
```yaml
id: dinamitero
nombre: Dinamitero
tipo: unidad_jugador
rol: defensivo
obtencion: Recluta especial / edificio minero (por definir)
funcion_dia: Puede abrir zonas bloqueadas del mapa (por definir)
funcion_noche: Daño en área contra grupos y tanques
arma_base: dinamita
raptable: true
stats: {vida: TBD, dano: aoe_alto, cadencia: muy_lenta, rango: medio, velocidad: TBD}
costo: {madera: 0, chatarra: TBD, comida_upkeep: TBD}
mejoras: [mecha corta (más cadencia), barril (más área)]
notas_diseno: Riesgo de fuego amigo cómico — parte del tono del juego.
estado: propuesta
```

### 1.8 doctor
```yaml
id: doctor
nombre: Doctor / Curandero
tipo: unidad_jugador
rol: economico
obtencion: Recluta especial
funcion_dia: Cura unidades heridas; acelera la recuperación del héroe Malherido
funcion_noche: Atiende un puesto médico tras las líneas
arma_base: ninguna
raptable: true
stats: {vida: TBD, dano: 0, cadencia: n/a, rango: n/a, velocidad: TBD}
costo: {madera: 0, chatarra: TBD, comida_upkeep: TBD}
mejoras: [elixires dudosos (buff temporal aleatorio, tono Weird West)]
notas_diseno: Conecta con el sistema de derribo del héroe (GDD §4.1).
estado: propuesta
```

### 1.9 sheriff
```yaml
id: sheriff
nombre: Sheriff
tipo: unidad_jugador
rol: defensivo
obtencion: Evento / nivel de pueblo alto
desbloqueo_objetivo: TBD (candidato a objetivo propio, §8)
funcion_dia: Patrulla, disuade eventos negativos (por definir)
funcion_noche: Mini-héroe que ancla un flanco; buff de moral en su zona
arma_base: revolver_doble
raptable: true
stats: {vida: alta, dano: TBD, cadencia: TBD, rango: medio, velocidad: TBD}
costo: {madera: 0, chatarra: 0, comida_upkeep: TBD}
mejoras: [TBD]
notas_diseno: Único por pueblo. Su rapto es un evento dramático.
estado: propuesta
```

---

## 2. Enemigos

> **Cambio canónico v0.2 — a quién le roban.** Ya no hay muro que atravesar: el
> alien entra por su flanco y va directo al **edificio-refugio más cercano** que
> contenga lo que busca (gente, ganado o recursos). Sacar cada víctima le lleva
> tiempo — 1–3 s por persona, 2 s por recurso, ganado `TBD` — y durante esa
> ventana está quieto y expuesto. Matarlo antes le cancela el robo; matarlo
> cargado le hace soltar lo que lleva. Las reglas completas están en
> [§5.0](#50-reglas-de-los-edificios-de-noche-cambio-canónico), porque son
> reglas del edificio tanto como del enemigo.

## 2.1 Categoría: LADRON
> Comportamiento base: entra por un flanco, corre al **edificio-refugio** o recurso suelto más cercano, saquea lo que pueda (con el tiempo de robo de §5.0) y huye por donde vino. Frágil, veloz, en grupo.

### 2.1.1 ratero_gris
```yaml
id: ratero_gris
nombre: Ratero Gris
tipo: enemigo
categoria: ladron
que_roba: recursos
como_roba: Corre al edificio-refugio o recurso suelto más cercano, tarda 2 s en cargar cada recurso y huye. Si lo matan durante esos 2 s no se lleva nada
contramedida: Cualquier defensa lo mata; el reto es el volumen del grupo y que hay que llegarle mientras saquea
movimiento: terrestre
aparicion: noche 1+
tiempo_robo: default (2 s por recurso, §5.0)
stats: {vida: baja, dano: nulo, velocidad: alta, capacidad_robo: 1_recurso}
drops: [componente_comun (baja probabilidad)]
comportamiento_amanecer: huye con lo que cargue
notas_diseno: El enemigo tutorial. Enseña la regla central — te roban, no te matan — y con v0.2 enseña también la segunda mitad de la regla: robar lleva tiempo, y ese tiempo es tu oportunidad.
estado: canon
```

### 2.1.2 coyote_plateado
```yaml
id: coyote_plateado
nombre: Coyote Plateado
tipo: enemigo
categoria: ladron
que_roba: comida
como_roba: Muy rápido, esquiva en zigzag; prioriza la granja y el establo, que de noche son los refugios donde están la comida, el pasto y las vacas
contramedida: Escopetas (área) y trampas; las balas simples fallan por su esquiva
movimiento: terrestre
aparicion: noche 2+
tiempo_robo: default (2 s por recurso, §5.0)
stats: {vida: baja, dano: bajo, velocidad: muy_alta, capacidad_robo: TBD}
drops: [componente_comun]
comportamiento_amanecer: huye con lo que cargue
notas_diseno: Bestia terrestre alienizada. Introduce la idea de contramedidas específicas.
estado: canon
```

### 2.1.3 manos_largas
```yaml
id: manos_largas
nombre: Manos Largas
tipo: enemigo
categoria: ladron
que_roba: recursos
como_roba: Brazos elásticos que entran al refugio DESDE AFUERA — saquea por la ventana sin cruzar la puerta, así que los defensores de adentro no lo alcanzan. Si el modo clásico de muros está activo (§5.8), roba además por encima de las barricadas bajas sin romperlas
contramedida: Eliminarlo a distancia, o una torre configurada con prioridad `ya_cargado` (§5.0) — es el enemigo que justifica esa opción
movimiento: terrestre
aparicion: noche 4+
tiempo_robo: default (§5.0)
stats: {vida: media, dano: nulo, velocidad: media, capacidad_robo: TBD}
drops: [componente_comun, componente_raro (baja)]
comportamiento_amanecer: huye con lo que cargue
notas_diseno: Su función era atacar la sensación de seguridad del muro; sin muros por defecto (v0.2) pasa a atacar la sensación de seguridad del REFUGIO — el edificio deja de ser un búnker. Vuelve a `propuesta` porque el mecanismo se reescribió y hay que validarlo en prototipo.
estado: propuesta
```

## 2.2 Categoría: ABDUCTOR
> Comportamiento base: se lleva lo VIVO (ganado, personas). Regla universal: si derribas al abductor antes de que salga de pantalla, la víctima cae VIVA y se recupera. Si escapa, se perdió para siempre.

### 2.2.1 platillo_sonda
```yaml
id: platillo_sonda
nombre: Platillo Sonda
tipo: enemigo
categoria: abductor
que_roba: ganado
como_roba: OVNI pequeño con rayo tractor LENTO sobre vacas; de noche las vacas están guardadas en el establo (§5.3), así que tiene que sacarlas de ahí primero. La lentitud da ventana de reacción
contramedida: Cualquier DPS aéreo básico (cazadores, torres)
movimiento: volador
aparicion: noche 3+
tiempo_robo: TBD — el tiempo de extracción del ganado no está decidido (§9, D3)
stats: {vida: baja, dano: nulo, velocidad: baja, capacidad_robo: 1_vaca}
drops: [componente_comun, componente_antigrav (media)]
comportamiento_amanecer: huye con lo que cargue
notas_diseno: Primera imagen icónica del juego — la vaca flotando. Cómico Y amenazante. Enseña la mecánica de rescate por derribo.
estado: canon
```

### 2.2.2 platillo_abductor
```yaml
id: platillo_abductor
nombre: Platillo Abductor
tipo: enemigo
categoria: abductor
que_roba: personas
como_roba: Rayo tractor sobre unidades; se planta sobre el refugio y tarda 1-3 s en sacar a la persona antes de subirla. Escudo frontal — vulnerable por detrás
contramedida: Cazadores posicionados, arpón antigravedad (T3)
movimiento: volador
aparicion: noche 6+
tiempo_robo: default (1-3 s por persona, §5.0)
stats: {vida: media, dano: nulo, velocidad: media, capacidad_robo: 1_persona}
drops: [componente_raro, componente_antigrav]
comportamiento_amanecer: huye con lo que cargue
notas_diseno: La escalada del Sonda: ahora se lleva a TU GENTE. El escudo direccional premia el posicionamiento.
estado: canon
```

### 2.2.3 sombrero_negro
```yaml
id: sombrero_negro
nombre: Sombrero Negro
tipo: enemigo
categoria: abductor
que_roba: personas
como_roba: Alien disfrazado de forastero; se infiltra caminando de noche, hipnotiza a un aldeano y "se lo lleva caminando" — las torres no lo detectan como hostil
contramedida: La Torre de Vigilancia lo revela; una vez revelado, cualquier defensa
movimiento: terrestre
aparicion: noche 7+
tiempo_robo: n/a — no saquea el refugio. Entra caminando, convence a la víctima y salen juntos, así que no genera la ventana de §5.0
stats: {vida: media, dano: nulo, velocidad: baja, capacidad_robo: 1_persona}
drops: [componente_raro]
comportamiento_amanecer: huye con lo que cargue
notas_diseno: El enemigo de terror del juego. No es fuerte — es que no lo VES. Justifica la existencia de la Torre de Vigilancia y crea paranoia ("¿ese es de los nuestros?"). Con v0.2 gana un segundo filo: es el único que ignora la ventana de robo, así que las torres nunca lo pillan saqueando.
estado: canon
```

## 2.3 Categoría: TANQUE
> Comportamiento base: no roba — ROMPE. Existía para destruir barricadas y abrir camino a los demás; **sin muros por defecto (v0.2) su blanco pasa a ser lo que sí estorba: las torres colocadas y la estructura de los edificios-refugio.** Romper un refugio no destruye lo que hay dentro: lo deja al descubierto y acelera el saqueo de los ladrones. Las tres fichas de esta categoría vuelven a `propuesta` mientras el nuevo blanco no se valide en prototipo.

### 2.3.1 toro_de_marte
```yaml
id: toro_de_marte
nombre: Toro de Marte
tipo: enemigo
categoria: tanque
que_roba: nada (rompe)
como_roba: n/a — embiste con carga telegrafiada las torres y las puertas de los edificios-refugio; reventar un refugio deja a la gente y los recursos de adentro expuestos para los ladrones que vienen detrás
contramedida: Daño concentrado durante el telegraph; dinamita
movimiento: terrestre
aparicion: noche 5+
tiempo_robo: n/a
stats: {vida: alta, dano: alto_vs_estructuras, velocidad: baja_con_cargas, capacidad_robo: 0}
drops: [componente_raro, placa_blindaje]
comportamiento_amanecer: huye
notas_diseno: Espejo alienígena del ganado que te roban — un toro, pero suyo. Era la primera amenaza real a los muros; ahora es la primera amenaza real al refugio, que es peor, porque el muro se reconstruye y la gente de adentro no. Vuelve a `propuesta` por el cambio de blanco.
estado: propuesta
```

### 2.3.2 caparazon
```yaml
id: caparazon
nombre: Caparazón
tipo: enemigo
categoria: tanque
que_roba: nada (rompe)
como_roba: n/a — avanza lento con blindaje frontal total, golpea torres y edificios; absorbe el fuego de las torres mientras los ladrones saquean detrás suyo
contramedida: Flanqueo, daño en área, armas de plasma T3 (ignoran armadura)
movimiento: terrestre
aparicion: noche 8+
tiempo_robo: n/a
stats: {vida: muy_alta, dano: medio_vs_estructuras, velocidad: muy_baja, capacidad_robo: 0}
drops: [placa_blindaje, componente_raro]
comportamiento_amanecer: huye
notas_diseno: Chequeo de progresión — si no has avanzado el árbol tecnológico, este enemigo te lo cobra. Sin muros su rol se afila como escudo móvil del grupo, y por eso su lectura depende de la decisión abierta D1 (§9) sobre si las torres atraen al enemigo o no.
estado: propuesta
```

### 2.3.3 demoledor
```yaml
id: demoledor
nombre: Demoledor
tipo: enemigo
categoria: tanque
que_roba: nada (rompe)
como_roba: n/a — lanza proyectiles de asedio contra torres desde media distancia, fuera del rango de defensas cortas
contramedida: Salir a cazarlo con el héroe/pistoleros, o fuego de largo alcance (cazadores)
movimiento: terrestre
aparicion: noche 9+
tiempo_robo: n/a
stats: {vida: media, dano: alto_vs_torres, velocidad: baja, capacidad_robo: 0}
drops: [componente_raro, nucleo_asedio]
comportamiento_amanecer: huye
notas_diseno: Rompe el turtling. Su blanco ya era la torre, así que es el tanque que menos cambia con v0.2 — pero ahora que las torres son colocables donde el jugador quiera, castiga directamente el amontonarlas en un solo punto. Vuelve a `propuesta` junto con el resto de la categoría.
estado: propuesta
```

## 2.4 Categoría: SOPORTE
> Comportamiento base: no roba ni rompe — POTENCIA a los demás. Prioridad de fuego alta. "Los magos" de la invasión.

### 2.4.1 psiquico_velado
```yaml
id: psiquico_velado
nombre: Psíquico Velado
tipo: enemigo
categoria: soporte
que_roba: nada (potencia)
como_roba: n/a — proyecta escudos de energía sobre otros aliens cercanos
contramedida: Matarlo primero; los escudos caen con él
movimiento: terrestre
aparicion: noche 8+
stats: {vida: baja, dano: nulo, velocidad: baja, capacidad_robo: 0}
drops: [componente_raro, cristal_psiquico]
comportamiento_amanecer: huye
notas_diseno: Cambia la prioridad de objetivos. Su silueta debe leerse a distancia y dar miedo verla llegar.
estado: canon
```

### 2.4.2 reparador
```yaml
id: reparador
nombre: Reparador
tipo: enemigo
categoria: soporte
que_roba: nada (potencia)
como_roba: n/a — dron que cura/repara tanques y naves aliadas
contramedida: Cazadores (es volador y frágil)
movimiento: volador
aparicion: noche 9+
stats: {vida: baja, dano: nulo, velocidad: alta, capacidad_robo: 0}
drops: [componente_comun, herramienta_alien]
comportamiento_amanecer: huye
notas_diseno: Espejo de tu propia mecánica de reparación en combate — ellos también reparan bajo fuego.
estado: canon
```

### 2.4.3 hipnotizador
```yaml
id: hipnotizador
nombre: Hipnotizador
tipo: enemigo
categoria: soporte
que_roba: nada (potencia)
como_roba: n/a — canaliza sobre una unidad tuya y la voltea temporalmente (pelea en tu contra; NO puede ser raptada mientras está volteada)
contramedida: Dañarlo rompe el canal y libera a la unidad
movimiento: terrestre
aparicion: noche 10+
stats: {vida: media, dano: nulo, velocidad: baja, capacidad_robo: 0}
drops: [cristal_psiquico, componente_raro]
comportamiento_amanecer: huye (la unidad volteada se libera)
notas_diseno: Drama sin pérdida permanente — ver a tu cazador dispararle a tus peones es terrible, pero reversible.
estado: canon
```

### 2.4.4 faro_lunar
```yaml
id: faro_lunar
nombre: Faro Lunar
tipo: enemigo
categoria: soporte
que_roba: nada (potencia)
como_roba: n/a — amplifica la transformación lunar de los aliens cercanos durante la luna llena
contramedida: Objetivo prioritario absoluto del "examen" de luna llena
movimiento: terrestre
aparicion: solo luna llena
stats: {vida: alta, dano: nulo, velocidad: muy_baja, capacidad_robo: 0}
drops: [cristal_lunar (garantizado), componente_raro]
comportamiento_amanecer: huye
notas_diseno: Ancla mecánica del ciclo lunar (GDD §9). Su drop garantizado hace que las lunas llenas también sean oportunidad, no solo castigo.
estado: canon
```

## 2.5 Categoría: JEFE

### 2.5.1 nave_capataz
```yaml
id: nave_capataz
nombre: Nave Capataz
tipo: enemigo
categoria: jefe
que_roba: personas y ganado (masivo)
como_roba: Rayo tractor masivo capaz de levantar varias víctimas; abre el techo de un edificio-refugio entero y vacía lo que haya dentro. Llega con escolta de abductores y soporte
contramedida: Concentrar antiaéreo; derribarla suelta TODO lo que cargue
movimiento: volador
aparicion: lunas llenas (mini-jefe recurrente)
tiempo_robo: default por víctima (§5.0), pero saca varias en paralelo
stats: {vida: muy_alta, dano: medio, velocidad: baja, capacidad_robo: multiple}
drops: [componente_epico, componente_antigrav x3]
comportamiento_amanecer: huye con todo lo que cargue
notas_diseno: El "examen" de luna llena hecho carne. Derribarla cargada es el momento más satisfactorio del mid-game — llueven vacas y aldeanos vivos.
estado: canon
```

### 2.5.2 el_ganadero
```yaml
id: el_ganadero
nombre: El Ganadero
tipo: enemigo
categoria: jefe
que_roba: nada (rompe) — pero su nombre es la amenaza
como_roba: Coloso que "cosecha" — arranca del suelo las torres colocadas (y las barricadas, si el modo clásico está activo) y las usa como arma contra el resto de tus defensas
contramedida: TBD — pelea de jefe mid-game con fases
movimiento: terrestre
aparicion: evento mid-game (noche ~10, por definir)
tiempo_robo: n/a
stats: {vida: jefe, dano: muy_alto, velocidad: baja, capacidad_robo: 0}
drops: [componente_epico x2, nucleo_ganadero]
comportamiento_amanecer: huye (si sobrevive, vuelve la siguiente luna llena)
notas_diseno: Invierte la fantasía — el jugador es el ganado desde la perspectiva alien. Diseño de fases pendiente.
estado: propuesta
```

### 2.5.3 nave_nodriza
```yaml
id: nave_nodriza
nombre: Nave Nodriza
tipo: enemigo
categoria: jefe
que_roba: n/a — es el OBJETIVO FINAL, no ataca el pueblo
como_roba: n/a
contramedida: El jugador la ASALTA de día con héroe + milicia equipada con tecnología alien
movimiento: estatica (campo cercano, visible desde el inicio del run)
aparicion: presente desde la noche 1 (meta visible)
stats: {vida: jefe_final, dano: TBD, velocidad: 0, capacidad_robo: 0}
drops: [victoria]
comportamiento_amanecer: n/a
notas_diseno: "Fases del asalto: 1) Escudo perimetral (destruir generadores), 2) Torretas defensivas, 3) Núcleo expuesto. Destruirla = victoria del run."
estado: canon
```

---

## 3. Registro de componentes (drops)

| id | Rareza | Fuente principal | Usos |
|---|---|---|---|
| componente_comun | Común | Ladrones, drones | Recetas T1→T2, reparaciones |
| componente_raro | Raro | Abductores, tanques, soporte | Recetas T2→T3 |
| componente_epico | Épico | Jefes | Recetas T3 clave |
| componente_antigrav | Especial | Platillos | Arpón antigravedad, saco antigrav |
| placa_blindaje | Especial | Tanques | Barricadas T3, munición perforante |
| cristal_psiquico | Especial | Psíquicos, hipnotizadores | Torre de Vigilancia mejorada, contramedidas mentales |
| cristal_lunar | Especial | Faro Lunar (garantizado) | Recetas exclusivas del ciclo lunar (TBD) |
| nucleo_asedio | Especial | Demoledor | Torre de largo alcance |
| herramienta_alien | Especial | Reparador | Reparación automática de barricadas |
| nucleo_ganadero | Único | El Ganadero | TBD (recompensa de jefe) |

---

## 4. Armas

> Solo las armas que las fichas de unidad ya referencian por `arma_base`. El resto del árbol tecnológico (T1/T2/T3 de GDD §8.1) sigue en el backlog de §10.

### 4.1 revolver
```yaml
id: revolver
nombre: Revólver
tipo: arma
tier: T1_humano
montaje: unidad
fabricacion: Se fabrica en la Armería
efecto: Disparo a distancia de cadencia sostenida; convierte a un peón en pistolero
stats: {dano: TBD, cadencia: TBD, rango: TBD, area: n/a}
costo: {madera: TBD, chatarra: TBD, componentes: n/a}
mejoras: [ruta del árbol tecnológico T2 híbrido → T3 plasma (TBD)]
notas_diseno: Arma base del pistolero y primer eslabón del árbol tecnológico. Las armas alien serían mejoras de equipo sobre esta línea, no clases nuevas (pendiente de confirmar, GDD §13).
estado: propuesta
```

### 4.2 rifle_largo
```yaml
id: rifle_largo
nombre: Rifle largo
tipo: arma
tier: T1_humano
montaje: unidad
fabricacion: Se fabrica en la Armería (arma humana, GDD §6.2)
efecto: Disparo de largo alcance y cadencia lenta; alcanza voladores
stats: {dano: TBD, cadencia: TBD, rango: TBD, area: n/a}
costo: {madera: TBD, chatarra: TBD, componentes: n/a}
mejoras: [mira (más rango), munición perforante]
notas_diseno: Arma del cazador. De día caza animales para comida, de noche es la respuesta antiaérea temprana — por eso su alcance es el stat que la define.
estado: propuesta
```

### 4.3 lazo
```yaml
id: lazo
nombre: Lazo
tipo: arma
tier: TBD
montaje: unidad
fabricacion: Equipo propio del vaquero; llega con el Establo
efecto: Enlaza — puede jalar de vuelta ganado que está siendo abducido o inmovilizar aliens pequeños
stats: {dano: TBD, cadencia: TBD, rango: TBD, area: n/a}
costo: {madera: TBD, chatarra: TBD, componentes: n/a}
mejoras: [lazo reforzado]
notas_diseno: No figura en el árbol tecnológico de GDD §8.1 — es equipo de trabajo, no de guerra. Es la contramedida manual al platillo_sonda y su mecánica está a validar en prototipo (ver 1.5).
estado: propuesta
```

### 4.4 dinamita
```yaml
id: dinamita
nombre: Dinamita
tipo: arma
tier: T1_humano
montaje: unidad
fabricacion: Por definir — llega con el dinamitero (recluta especial / edificio minero)
efecto: Daño en área con mecha; castiga grupos y tanques
stats: {dano: TBD, cadencia: TBD, rango: TBD, area: TBD}
costo: {madera: TBD, chatarra: TBD, componentes: n/a}
mejoras: [mecha corta (más cadencia), barril (más área)]
notas_diseno: Única fuente de daño en área del T1 y contramedida citada contra el toro_de_marte. El riesgo de fuego amigo es cómico a propósito (ver 1.7).
estado: propuesta
```

### 4.5 revolver_doble
```yaml
id: revolver_doble
nombre: Revólver doble
tipo: arma
tier: TBD
montaje: unidad
fabricacion: No se fabrica — llega con el sheriff (evento / nivel de pueblo alto)
efecto: Par de revólveres; versión de mini-héroe del revólver, ancla un flanco
stats: {dano: TBD, cadencia: TBD, rango: TBD, area: n/a}
costo: {madera: TBD, chatarra: TBD, componentes: n/a}
mejoras: [TBD]
notas_diseno: No es una entrada propia del árbol tecnológico: es la variante que porta el sheriff, único por pueblo. Si lo raptan, el arma se va con él.
estado: propuesta
```

---

## 5. Edificios

> Los edificios de GDD §6.2. **Ya no hay línea de muros por defecto**: el rancho
> está abierto y son los propios edificios los que aguantan la noche (§5.0).

### 5.0 Reglas de los edificios de noche (cambio canónico)

Esta subsección es normativa: define el comportamiento base que heredan todas
las fichas de §5, igual que las categorías de §2 definen el de los enemigos.

**1. Todo edificio tiene dos vidas.** De día cumple su función económica
(`funcion_dia`). Al caer la noche se convierte en una de estas cosas
(`modo_noche`):

| `modo_noche` | Qué significa |
|---|---|
| `refugio` | La gente y los recursos se guardan adentro. Es lo que el alien viene a vaciar. |
| `defensa` | Dispara. No guarda a nadie. |
| `refugio_y_defensa` | Guarda **y** dispara. Es una mejora (§5.0.4), no un estado inicial. |
| `ninguno` | De noche no hace nada; queda como estructura vacía. |

**2. El rancho está abierto.** No hay muros de serie. La ficción lo explica:
la invasión es una sorpresa en un valle del oeste, no un asedio anunciado a un
castillo; nadie levantó una muralla porque nadie sabía que venía nadie. Los
aliens bajan de las naves y caminan hasta lo que quieren. La `barricada` (5.8)
sigue existiendo como **variante clásica opcional**, no como default.

**3. Robar cuesta tiempo, y ese tiempo es la ventana de defensa.** El alien no
"toca y desaparece": entra al **primer edificio-refugio que encuentra en su
camino** y se queda adentro cargando:

| Qué se lleva | Cuánto tarda |
|---|---|
| Una persona | **1–3 s** — el valor exacto se sortea una vez por oleada |
| Un recurso | **2 s** |

Mientras carga es un blanco quieto. Si muere ahí dentro, **suelta lo que ya
tenía encima** y la víctima se libera viva (misma regla que el abductor
derribado, §2.2). Vaciar un refugio entero de gente es caro en segundos: ese es
el presupuesto que el jugador le pelea con torres.

**4. Los edificios suben de nivel.** Con el árbol de habilidades y la tecnología
alien, un refugio puede ramificar:

- **`refugio_y_defensa`** — el edificio se arma: sigue guardando gente y además
  dispara a quien entre a robar.
- **`doble_refugio`** — el edificio no dispara, pero **duplica su capacidad**
  (más personas y más recursos adentro). Menos edificios que defender, más huevos
  en la misma canasta.

La rama se elige por edificio, no globalmente: dos graneros del mismo pueblo
pueden ir por caminos distintos.

**5. Las torres se colocan donde el jugador quiera** (`slot: libre`) y se
configuran con una `prioridad_objetivo`:

| Prioridad | A quién dispara primero |
|---|---|
| `primero_en_llegar` | Al alien que entró primero al edificio que la torre cubre |
| `mas_cercano_a_recursos` | Al que está por alcanzar un refugio cargado |
| `ya_cargado` | Al que ya lleva algo encima — matarlo devuelve el botín |

> ⚠️ **DECISIÓN ABIERTA — variante A / variante B.** Falta decidir qué hacen los
> aliens con las torres:
> **(A)** las atacan primero — la torre es un obstáculo que hay que resolver, o
> **(B)** las ignoran y van directo a los edificios — la torre nunca frena a
> nadie, solo mata mientras roban.
> Y si esto es **configurable** (dificultad / tipo de enemigo) o una sola de las
> dos. Cambia por completo dónde conviene poner una torre y qué significa
> `prioridad_objetivo`, así que **ninguna ficha la asume**. La decisión está
> anotada como **D1** en [§9](#9-decisiones-abiertas-para-el-equipo), junto con
> **D2** (si los muros estilo Kingdom entran como opción de partida).

### 5.1 town_center
```yaml
id: town_center
nombre: Town Center
tipo: edificio
funcion: Núcleo del rancho y almacén principal; el nivel del pueblo marca los desbloqueos
funcion_dia: Almacén central de recursos y centro de órdenes del pueblo
funcion_noche: Refugio principal — es el edificio con más recursos y más gente adentro
modo_noche: refugio
capacidad_refugio: TBD
prioridad_objetivo: n/a
slot: centro
obtencion: Presente desde el inicio del run
desbloquea: TBD
niveles: [refugio_y_defensa, doble_refugio]
stats: {vida: TBD, tiempo_construccion: n/a}
costo: {madera: n/a, chatarra: n/a}
notas_diseno: Es el refugio al que corre el ratero_gris si no hay nada más cerca en su camino. Concentrar todo en el centro es cómodo de cubrir con torres y catastrófico de perder. No se construye ni se compra (de ahí `n/a` en costo y tiempo); lo que desbloquea son los niveles de pueblo, que todavía no son entidades de la wiki.
estado: propuesta
```

### 5.2 taberna
```yaml
id: taberna
nombre: Taberna / Inn
tipo: edificio
funcion: Atrae y aloja reclutas; asignación de roles
funcion_dia: Atrae reclutas y permite reasignar roles a la población
funcion_noche: Refugio de personas — el objetivo más goloso de la noche por densidad de gente
modo_noche: refugio
capacidad_refugio: TBD
prioridad_objetivo: n/a
slot: lateral
obtencion: Construible en un slot del rancho
desbloquea: [peon]
niveles: [refugio_y_defensa, doble_refugio]
stats: {vida: TBD, tiempo_construccion: TBD}
costo: {madera: TBD, chatarra: TBD}
notas_diseno: Puerta de entrada de la población, que es el recurso vivo y el que más roban (GDD §5.1). De noche es el edificio donde el robo por persona (1–3 s, §5.0) más se nota: una taberna llena tarda mucho en vaciarse, y esa demora es lo que le da sentido a poner torres cerca.
estado: propuesta
```

### 5.3 establo
```yaml
id: establo
nombre: Establo / Corral
tipo: edificio
funcion: Aloja el ganado, lo saca a pastar de día y lo guarda de noche
funcion_dia: Los vaqueros sacan las vacas a pastar el pasto de alrededor; el ganado convierte pasto en comida
funcion_noche: Refugio de ganado — los trabajadores meten las vacas adentro y esperan la invasión
modo_noche: refugio
capacidad_refugio: TBD
prioridad_objetivo: n/a
slot: lateral
obtencion: Construible en un slot del rancho
desbloquea: [vaquero_ganado, lazo, vaca]
niveles: [refugio_y_defensa, doble_refugio]
stats: {vida: TBD, tiempo_construccion: TBD}
costo: {madera: TBD, chatarra: TBD}
notas_diseno: El corral es el blanco del platillo_sonda — la vaca flotando es la imagen icónica del juego. Cuanto más ganado, más rápido se come el pasto (ver vaca y pasto en §7): el establo grande no es gratis, es una boca más grande. Guardar las vacas de noche las protege del abductor pero las concentra en un solo refugio robable; el nivel doble_refugio agranda esa apuesta.
estado: propuesta
```

### 5.4 armeria
```yaml
id: armeria
nombre: Armería / Herrería
tipo: edificio
funcion: Fabrica y mejora armas humanas; equipa unidades
funcion_dia: Fabrica y mejora armas humanas; equipa a las unidades
funcion_noche: Refugio de gente y de armas; es el edificio que antes llega a refugio_y_defensa
modo_noche: refugio
capacidad_refugio: TBD
prioridad_objetivo: n/a
slot: lateral
obtencion: Construible en un slot del rancho
desbloquea: [pistolero, revolver, rifle_largo]
niveles: [refugio_y_defensa, doble_refugio]
stats: {vida: TBD, tiempo_construccion: TBD}
costo: {madera: TBD, chatarra: TBD}
notas_diseno: GDD §6.2 le asigna todas las armas humanas; hoy solo el revólver está atado a ella explícitamente por la ficha del pistolero. Que la armería sea el edificio natural para la rama refugio_y_defensa es ficción gratis: es el que ya tiene las armas adentro.
estado: propuesta
```

### 5.5 laboratorio
```yaml
id: laboratorio
nombre: Laboratorio del Profesor
tipo: edificio
funcion: Investiga tecnología alien y desbloquea las recetas del árbol tecnológico
funcion_dia: El científico investiga tecnología alien y desbloquea recetas del árbol
funcion_noche: Refugio del científico y de los componentes sin investigar
modo_noche: refugio
capacidad_refugio: TBD
prioridad_objetivo: n/a
slot: lateral
obtencion: Llega con el científico, que a su vez se desbloquea por objetivo (§8 y GDD §6.4)
desbloquea: [chatarrero, campo_fuerza_alien]
niveles: [refugio_y_defensa, doble_refugio]
stats: {vida: TBD, tiempo_construccion: TBD}
costo: {madera: TBD, chatarra: TBD}
notas_diseno: Sin científico el edificio no produce nada — raptarlo detiene la investigación (ver 1.6). Es el edificio cuyo valor depende de una unidad viva, y por eso el que peor tolera ser el refugio más cercano al flanco. También habilita las recetas del árbol tecnológico (GDD §8.1), que todavía no son fichas, y las mejoras de nivel de los demás edificios (§5.0.4).
estado: propuesta
```

### 5.6 torre_vigilancia
```yaml
id: torre_vigilancia
nombre: Torre de vigilancia
tipo: edificio
funcion: Torre defensiva colocable; recibe las armas del árbol tecnológico
funcion_dia: Vigila el horizonte y revela infiltrados; no produce recursos
funcion_noche: Dispara a los aliens, incluso mientras están robando dentro de un edificio
modo_noche: defensa
capacidad_refugio: 0
prioridad_objetivo: [primero_en_llegar, mas_cercano_a_recursos, ya_cargado]
slot: libre
obtencion: Se coloca donde el jugador quiera, sin línea de defensa fija (§5.0)
desbloquea: TBD
niveles: [mejorada con cristal_psiquico]
stats: {vida: TBD, tiempo_construccion: TBD}
costo: {madera: TBD, chatarra: TBD}
notas_diseno: Ya no vive en una línea de muros: se coloca libre, y decidir a qué edificio cubre es la decisión táctica del jugador. Matar a un ladrón mientras carga le hace soltar lo robado (§5.0.3), así que la torre no existe para frenar la invasión sino para cobrarle el tiempo que pasa adentro. Su prioridad_objetivo es configurable por torre. Revela al sombrero_negro: sin torre, el infiltrado camina entre tu gente sin que las defensas lo lean como hostil. Recibe las armas de montaje torre del árbol tecnológico (GDD §8.1), que todavía no son fichas. PENDIENTE: si los aliens la atacan (variante A) o la ignoran (variante B) — decisión abierta D1 de §9.
estado: propuesta
```

### 5.7 granja
```yaml
id: granja
nombre: Granja / Granero
tipo: edificio
funcion: Cultiva comida y hace crecer el pasto a su alrededor
funcion_dia: Produce comida de cultivo y genera pasto en el radio que la rodea, que es donde pastan las vacas
funcion_noche: Refugio de gente y de la comida almacenada
modo_noche: refugio
capacidad_refugio: TBD
prioridad_objetivo: n/a
slot: lateral
obtencion: Construible en un slot del rancho
desbloquea: [pasto]
niveles: [refugio_y_defensa, doble_refugio]
stats: {vida: TBD, tiempo_construccion: TBD, radio_pasto: TBD}
costo: {madera: TBD, chatarra: TBD}
notas_diseno: Segunda pata de la comida, para que perder el ganado no corte la única fuente — y ahora también la primera pata de la cadena del ganado, porque el pasto sale de acá (§7). Eso la vuelve un objetivo indirecto: vaciarte la granja no te mata las vacas hoy, te las deja sin comer en tres días. El coyote_plateado la prioriza. El nivel doble_refugio es el granero grande.
estado: propuesta
```

### 5.8 barricada
```yaml
id: barricada
nombre: Barricadas / Muros
tipo: edificio
funcion: Línea defensiva por niveles — VARIANTE CLÁSICA OPCIONAL, no el default (§5.0.2)
funcion_dia: Se construye, se repara y se empuja hacia afuera para expandir territorio
funcion_noche: Frena y encauza a los aliens terrestres hacia donde el jugador quiere
modo_noche: ninguno
capacidad_refugio: 0
prioridad_objetivo: n/a
slot: linea_defensa
obtencion: Solo si la partida se juega con la variante de muros estilo Kingdom (decisión abierta D2 de §9)
desbloquea: n/a
niveles: [madera, reforzada, tec alien (placa_blindaje)]
stats: {vida: TBD, tiempo_construccion: TBD}
costo: {madera: TBD, chatarra: TBD}
notas_diseno: DEGRADADA A OPCIÓN. El rancho abierto es el nuevo default y la defensa la sostienen los edificios-refugio más las torres colocables (§5.0). Esta ficha se conserva entera porque los muros estilo Kingdom siguen sobre la mesa como alternativa de partida, y porque tres enemigos canon se diseñaron contra ella (manos_largas, toro_de_marte, el_ganadero). Si la variante se descarta, esos tres se rediseñan y esta ficha se archiva. Se repara de noche bajo fuego y el reparador es raptable (GDD §6.3). No desbloquea entidades (de ahí `n/a`).
estado: propuesta
```

### 5.9 campo_fuerza_alien
```yaml
id: campo_fuerza_alien
nombre: Campo de fuerza alien
tipo: edificio
funcion: Barrera de energía T3 — la respuesta alienígena al muro, para el late game
funcion_dia: Inactivo; el emisor recarga con tecnología alien
funcion_noche: Levanta una barrera de energía entre dos emisores; los aliens no la cruzan mientras aguante
modo_noche: defensa
capacidad_refugio: 0
prioridad_objetivo: n/a
slot: libre
obtencion: Se fabrica cuando el árbol tecnológico está avanzado (T3, GDD §8.1); requiere laboratorio
desbloquea: n/a
niveles: TBD
stats: {vida: TBD, tiempo_construccion: TBD, energia: TBD, tiempo_recarga: TBD}
costo: {madera: TBD, chatarra: TBD}
notas_diseno: FICHA NUEVA, sin validar. Cierra el arco irónico del juego — no levantás una muralla de madera, levantás la misma tecnología con la que te robaron. Llega tarde a propósito: si estuviera disponible temprano, mataría la tensión del rancho abierto (§5.0.2). Pendiente de decidir si es una estructura (esta ficha) o el arma T3 barrera de energía de GDD §8.1 montada en torre; hoy se modela como estructura porque no dispara. Todos sus valores son TBD — no se inventan.
estado: propuesta
```

---

## 6. Oleadas

> Ficha de ejemplo para fijar la forma del tipo. La curva real (presupuesto por noche y costo en puntos por enemigo) está pendiente — ver el backlog de §10.

### 6.1 oleada_ejemplo
```yaml
id: oleada_ejemplo
nombre: Oleada de ejemplo
tipo: oleada
noche: TBD
fase_lunar: cualquiera
presupuesto: TBD
modificador_lunar: TBD
enemigos: los que cumplan su campo aparicion para esa noche y fase (nave_nodriza nunca entra)
spawn: {flancos: TBD, paths_voladores: TBD}
tiempos_robo: {persona_s: 1-3, recurso_s: 2}
determinista: true
notas_diseno: Plantilla, no balance. Existe para que el tipo oleada se ejercite de punta a punta en el pipeline mientras la curva real no está definida. Ninguna noche real debería referenciarla.
estado: propuesta
```

---

## 7. Recursos vivos y consumibles

> Tipo de ficha nuevo (`recurso`, §0). Existe porque la comida dejó de ser un
> número que sube solo: ahora es una cadena **pasto → vaca → comida**, y cada
> eslabón se puede cortar. Las materias primas que no tienen mecánica propia
> (madera, chatarra) siguen viviendo en GDD §5.1 como economía, no como fichas.

### 7.1 pasto
```yaml
id: pasto
nombre: Pasto / Forraje
tipo: recurso
clase: consumible
fuente: Crece de día en el radio que rodea a la granja; también hay parches naturales en el mapa
consumo: Las vacas lo pastan de día. Más vacas = se consume más rápido
robable: no — nadie se lleva el pasto; lo que se pierde es el ganado que lo come
funcion_dia: Se produce y se consume al mismo tiempo; el saldo del día decide si el ganado come
funcion_noche: No crece. Las vacas están guardadas, así que tampoco se consume
stats: {produccion: TBD, consumo_por_unidad: TBD, capacidad: TBD}
notas_diseno: FICHA NUEVA, sin validar. Es el freno natural al ganado: no podés escalar vacas sin escalar granjas, porque el rebaño se come su propio pasto. Convierte "tener muchas vacas" en una decisión con costo en vez de en una acumulación gratis, y le da a la granja un rol de infraestructura y no solo de comida. Ritmo de crecimiento y consumo son TBD — el equilibrio exacto entre vacas y granjas es justamente lo que hay que balancear.
estado: propuesta
```

### 7.2 vaca
```yaml
id: vaca
nombre: Vaca
tipo: recurso
clase: vivo
fuente: Se alojan en el establo; se compran o se encuentran explorando (por definir)
consumo: Come pasto de día; si no hay pasto pasa hambre y deja de producir comida
robable: si — el platillo_sonda la levanta con rayo tractor y el ratero entra al establo a llevársela
funcion_dia: Pasta en el radio de la granja y convierte pasto en comida
funcion_noche: La guardan en el establo; adentro está a salvo del abductor pero expuesta al ladrón que entre a robar
stats: {produccion: TBD, consumo_por_unidad: TBD, capacidad: TBD}
notas_diseno: FICHA NUEVA, sin validar — estaba pendiente en el backlog de la wiki desde v0.1. La vaca es la unidad de medida emocional del juego: es lo que se ve flotando en el rayo tractor y es lo que desbloquea gente (el científico llega cuando el rancho llega a X vacas, GDD §6.4). El hambre le agrega la segunda forma de perderla: no te la roban, se te muere de a poco porque construiste mal. Si un abductor cargado cae, la vaca cae viva (§2.2).
estado: propuesta
```

---

## 8. Objetivos de desbloqueo

> Cambio de v0.2: las entidades dejan de aparecer por "nivel de pueblo" o
> "renombre" difusos. Se desbloquean **cumpliendo objetivos concretos y
> legibles** — el jugador sabe qué le falta y por qué. El campo
> `desbloqueo_objetivo` de la ficha de unidad (§0) apunta acá.

| id del objetivo | Condición | Desbloquea | Estado |
|---|---|---|---|
| `objetivo_cientifico` | Sostener **X vacas vivas** en el rancho (X = `TBD`, ver §9 D4) | [`cientifico`](#16-cientifico) — y con él el `laboratorio` y el árbol tecnológico | propuesta |
| `objetivo_sheriff` | `TBD` — candidato: sobrevivir N noches sin perder gente | [`sheriff`](#19-sheriff) | propuesta |
| `objetivo_doctor` | `TBD` | [`doctor`](#18-doctor) | propuesta |

- Un objetivo **no se compra**: se cumple jugando. Es la manera de que criar
  ganado o proteger gente sea progresión y no solo economía.
- Los objetivos todavía **no son un tipo de ficha**: viven en esta tabla hasta
  que haya suficientes como para que valga un esquema propio (§10).
- Ninguna condición numérica se inventa acá: las X son `TBD` hasta balance
  (regla 1 de §0).

---

## 9. Decisiones abiertas para el equipo

> Estas son las preguntas que el cambio de mecánica de v0.2 dejó abiertas.
> **Nadie las resuelve por su cuenta** — las decide el equipo (Mato). Cada
> ficha que depende de una la referencia por su `Dn`.

| # | Decisión | Por qué importa | Quién depende |
|---|---|---|---|
| **D1** | **Variante A o B de las torres.** (A) Los aliens **atacan las torres primero** — la torre es un obstáculo que hay que resolver. (B) Las torres **no detienen a nadie**: los aliens van directo a los edificios y la torre solo les dispara mientras roban. ¿Y es **configurable** (por dificultad o por tipo de enemigo) o se elige una sola? | Cambia por completo dónde conviene colocar una torre, qué significa `prioridad_objetivo` y si el `caparazon` funciona como escudo móvil | [`torre_vigilancia`](#56-torre_vigilancia), [`caparazon`](#232-caparazon), [`demoledor`](#233-demoledor), §5.0.5 |
| **D2** | **¿Entran los muros estilo Kingdom como opción de partida?** El default ya está decidido (rancho abierto). Falta decidir si la variante clásica se ofrece como modo/opción o se descarta | Si se descarta, tres enemigos canon se quedan sin su razón de ser y hay que rediseñarlos | [`barricada`](#58-barricada), [`manos_largas`](#213-manos_largas), [`toro_de_marte`](#231-toro_de_marte), [`el_ganadero`](#252-el_ganadero) |
| **D3** | **¿Cuánto tarda un alien en sacar una vaca?** Persona (1–3 s) y recurso (2 s) están decididos; el ganado no. ¿Es más lento por ser grande, o instantáneo por el rayo tractor? | Define si el establo es defendible o si la vaca se pierde antes de que la torre dispare | [`platillo_sonda`](#221-platillo_sonda), [`establo`](#53-establo), [`vaca`](#72-vaca) |
| **D4** | **¿Cuántas vacas hacen falta para que llegue el científico?** Y qué otros objetivos de desbloqueo existen además de los tres de §8 | Es la primera puerta de progresión del run; si el número está mal, el árbol tecnológico llega tarde o regalado | [`cientifico`](#16-cientifico), §8 |
| **D5** | **El campo de fuerza alien: ¿estructura o arma?** Hoy se modela como edificio (§5.9) porque no dispara; GDD §8.1 lo lista como arma T3 "barrera de energía" montable en torre | Decide si el late game tiene una "muralla alien" o solo torres mejores | [`campo_fuerza_alien`](#59-campo_fuerza_alien) |
| **D6** | **Rama de nivel por edificio o global.** §5.0.4 asume que cada edificio elige por separado entre `refugio_y_defensa` y `doble_refugio`. ¿Es así, o el árbol de habilidades sube a todos los edificios de un tipo a la vez? | Cambia el costo de la progresión y cuánto micro tiene el jugador | Todas las fichas de §5 |

Cuando una decisión se cierre: se escribe acá el resultado, se actualizan las
fichas que la referencian y recién ahí el GDD resume el cambio.

---

## 10. Backlog de fichas pendientes
- [ ] Armas del árbol tecnológico como fichas (T1/T2/T3) con costos en componentes — §4 solo cubre las armas ya referenciadas por `arma_base`
- [ ] Curva de oleadas real: presupuesto por noche × modificador lunar, y el costo en puntos como campo de la ficha de enemigo (TECH §3.3)
- [x] Ganado como entidad → `vaca` (§7.2), con la cadena del `pasto` (§7.1). Faltan variantes de ganado, si las hay
- [ ] Variantes de luna llena de cada enemigo (sufijo `_lunar`: stats modificados)
- [ ] Valores de balance de todos los `TBD` (tras prototipo)
- [ ] Reconciliar los tres enemigos diseñados contra muros (`manos_largas`, `toro_de_marte`, `el_ganadero`) con el rancho abierto de §5.0 — depende de la decisión de muros opcionales
- [ ] Fichas de objetivo/desbloqueo (GDD §6.4): "X vacas → llega el científico" hoy es prosa, no entidad

---

*Wiki v0.2 — 9 unidades, 16 enemigos, 5 armas, 9 edificios, 1 oleada, 2 recursos, 10 componentes. Fuente canónica: cambios de diseño se hacen aquí primero y se resumen en el GDD.*
