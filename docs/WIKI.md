# COWBOY DEFENSE — Wiki de Entidades v0.2

> **Propósito:** Fuente canónica de todas las entidades del juego (unidades del jugador, enemigos, armas, edificios, oleadas). Este documento está estructurado para ser **consumido por sistemas de IA** que generen la wiki pública, assets, código de datos (ScriptableObjects / Resources) o contenido de balance.
> **Documentos hermanos:** [`GDD.md`](GDD.md) (diseño general) · [`TECH.md`](TECH.md) (técnico)
> **Navegación:** [índice de la wiki](wiki/README.md) — tablas por categoría con enlaces a cada ficha (generado, no editar a mano).

> ### ⚠️ v0.2 — cambio de mecánica del núcleo defensivo
> El equipo decidió (agosto 2026) que **el rancho no tiene muros**: la
> invasión es sorpresa, todo está abierto y los aliens bajan de sus naves. La
> defensa pasa a ser **edificios-refugio + torres colocables**, y el robo deja de
> ser "pasar el muro" para ser "entrar al refugio y tardar en sacar lo que hay"
> ([§5.0](#50-reglas-de-los-edificios-de-noche-cambio-canónico)).
>
> **Mato cerró las seis decisiones abiertas (29 de agosto de 2026):** las torres
> se atacan (variante A), no hay muros ni variante clásica, el robo tarda
> **3–5 s por cosa** y los aliens grandes se llevan **dos**, el campo de fuerza
> es un **desbloqueo post-científico que se paga con piezas alien** —y esas
> piezas se juntan en un **barrido diurno** nuevo—, y el árbol de talentos es
> **por edificio**. La sexta (**D4**) pasó por una fase de balance y también
> quedó cerrada: la **curva de progresión del científico** está aprobada en su
> forma —cuatro compuertas, el `doctor` en la segunda y un **respiro de 2–3
> noches suaves tras la luna llena**— con **todos sus valores todavía `TBD`**
> (`TASK-021`). El resultado está registrado en
> [§9](#9-decisiones-registradas-y-lo-que-sigue-abierto), la curva en
> [§8.1](#81-curva-de-progresión-del-científico--canon-d4-aprobada-por-mato).
> Resumen de diseño en [GDD §6](GDD.md#6-el-rancho-base).
>
> **Además (29 de agosto de 2026): el héroe tiene clase.** Mato definió **tres
> clases** —Sheriff (ataque), Alcalde (economía), Carpintero (defensa y
> capacidad)— que además son el marco de la meta-progresión roguelite entre
> runs. Fichas en [§11](#11-clases-del-héroe), séptimo esquema en
> [§0](#0-instrucciones-para-sistemas-de-ia), resumen en
> [GDD §4.3](GDD.md#43-clases-del-héroe-definido).

---

## 0. Instrucciones para sistemas de IA

Si eres una IA procesando este documento:

1. Cada entidad es una **ficha** con esquema fijo. Los campos con valor `TBD` están pendientes de balance — no los inventes salvo que se te pida explícitamente proponer valores.
2. El campo `id` es el identificador canónico (snake_case, estable): úsalo para nombres de archivo, clases, claves de datos y referencias cruzadas.
3. Las categorías de enemigos (`ladron`, `abductor`, `tanque`, `soporte`, `jefe`) definen comportamiento base heredable; la ficha solo describe lo que difiere.
4. La regla de diseño de todo enemigo: **quiere llevarse algo**. Si generas enemigos nuevos, deben responder: ¿qué roba, cómo lo roba, cómo se evita?
5. Tono del universo: Weird West 1870s, cómic pulp — gracioso en la superficie, inquietante en la incertidumbre. Sin gore.
6. Al generar contenido nuevo, mantén los campos del esquema y marca la ficha con `estado: propuesta`.
7. `estado: archivada` marca una ficha que el diseño **descartó** y que se conserva como referencia histórica (hoy solo la [`barricada`](#58-barricada), tras cerrarse D2): no se usa en partida ni se genera contenido nuevo a partir de ella.

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
slot:          # centro | lateral | libre (colocable donde el jugador quiera,
               # GDD §6.1). `linea_defensa` quedó sin uso al cerrarse D2.
obtencion:     # cómo se habilita o se construye
desbloquea:    # SOLO ids de esta wiki, en lista. Si lo que habilita todavía no
               # es una ficha, va `TBD`; si no habilita entidades, va `n/a`.
               # Lo que quede fuera se explica en `notas_diseno`. Esta lista es
               # verificable por referencia cruzada (TASK-009): nada de prosa.
niveles:       # progresión de mejora del edificio. Cada edificio tiene su
               # PROPIO árbol de talentos (D6, §5.0.4): la primera bifurcación
               # son las dos ramas canónicas refugio_y_defensa y doble_refugio,
               # y se pagan con árbol de habilidades + tecnología alien.
stats: {vida: TBD, tiempo_construccion: TBD}
costo: {madera: TBD, chatarra: TBD}
notas_diseno:  # intención de diseño
estado:        # canon | propuesta | archivada
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
tiempos_robo: {objeto_s: 3-5, multiplicador_grande: TBD}  # cuánto tarda un alien
                   # dentro de un edificio por cada cosa que se lleva —aldeano,
                   # comida o vaca— (§5.0, D3). El valor se sortea dentro del
                   # rango una vez por oleada. Un alien grande se lleva DOS
                   # cosas y tarda más: el multiplicador es TBD.
determinista: true # la composición se resuelve con el seed del run (TECH §3.3)
notas_diseno:      # intención de diseño
estado:            # canon | propuesta
```
> El **costo en puntos de cada enemigo** no vive acá: es un campo de la ficha de enemigo, todavía sin definir (ver el backlog de §10). La oleada solo aporta el presupuesto y el marco de spawn.

### Esquema de ficha — Clase de héroe
```yaml
id:            # snake_case canónico
nombre:        # nombre en español
tipo: clase_heroe
bonus:         # ataque | economia | defensa_capacidad — UN solo eje por clase
alcance:       # sobre qué aplica el bonus (edificios, unidades, recursos…)
funcion_dia:   # qué cambia en la gestión diurna
funcion_noche: # qué cambia en la defensa nocturna
stats: {magnitud_bonus: TBD, escalado_por_nivel: TBD}
meta_progresion: # cómo se mejora la clase o se desbloquean héroes de ella entre
               # runs (GDD §8.3). La mejora es permanente; la clase se elige
               # al empezar cada run
notas_diseno:  # intención de diseño
estado:        # canon | propuesta
```
> **Séptimo esquema** (29 de agosto de 2026, decisión de Mato). El héroe del
> jugador no es una unidad más ([§1](#1-unidades-del-jugador) son las que
> reclutás): es el personaje que controlás, y su **clase** es un multiplicador
> global sobre el rancho. Las tres clases viven en
> [§11](#11-clases-del-héroe). En coop cada héroe lleva su propia clase y los
> bonus **conviven sobre el mismo rancho** — cómo se apilan dos clases iguales
> es `TBD` de balance, no se inventa.

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
notas_diseno: La sangre del pueblo y el objetivo favorito de los Ladrones. Su pérdida frena toda la economía. Desde v0.2 el peón de noche no defiende un muro sino que ES el botín que hay dentro del refugio — sacarlo de ahí lleva 3-5 s al alien (§5.0), y esa ventana es lo que tus torres aprovechan. De mañana es también el que sale a barrer los restos de las naves caídas y trae las piezas alien (§7.3).
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
notas_diseno: Si te lo raptan, la investigación se DETIENE. Es la unidad más valiosa y más frágil — protegerlo es una decisión de layout. Desde v0.2 su llegada es un OBJETIVO explícito y no un umbral difuso de renombre — el ranchero que junta vacas se gana al científico, que es la manera del juego de decir "criar ganado también es progresión tecnológica". Con D4 aprobada su llegada dejó de ser un umbral suelto: es la CUARTA y última compuerta de la curva de progresión (§8.1), y exige tener cumplidas las tres previas. El número de vacas sigue TBD (§9.2).
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
obtencion: Objetivo de desbloqueo — llega cuando el rancho sostiene su población sin perder gente (§8.1, compuerta C2 cp_poblacion_sostenida)
desbloqueo_objetivo: objetivo_doctor
funcion_dia: Cura unidades heridas; acelera la recuperación del héroe Malherido
funcion_noche: Atiende un puesto médico tras las líneas
arma_base: ninguna
raptable: true
stats: {vida: TBD, dano: 0, cadencia: n/a, rango: n/a, velocidad: TBD}
costo: {madera: 0, chatarra: TBD, comida_upkeep: TBD}
mejoras: [elixires dudosos (buff temporal aleatorio, tono Weird West)]
notas_diseno: Conecta con el sistema de derribo del héroe (GDD §4.1). D4 le dio su desbloqueo definitivo — Mato confirmó que el doctor llega en la SEGUNDA compuerta de la curva de progresión (§8.1), la de población sostenida, "para que pueda sobrevivir hasta el final". Es la recompensa de defender gente, que es lo que más duele perder: el eje que premia lo mismo que te lo hace ganar. Los umbrales de C2 (P2_poblacion, P2_perdidas_max, P2_ventana) siguen pendientes de balance (§9.2).
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
> contenga lo que busca (gente, ganado o recursos). Sacar cada cosa le lleva
> tiempo — **3–5 s**, sea un aldeano, comida o una vaca — y durante esa
> ventana está quieto y expuesto. Los aliens **grandes** se llevan **dos** cosas
> en vez de una, y tardan más. Matarlo antes le cancela el robo; matarlo
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
como_roba: Corre al edificio-refugio o recurso suelto más cercano, tarda 3-5 s en cargar el recurso y huye. Si lo matan durante esa ventana no se lleva nada
contramedida: Cualquier defensa lo mata; el reto es el volumen del grupo y que hay que llegarle mientras saquea
movimiento: terrestre
aparicion: noche 1+
tiempo_robo: default (3-5 s por cosa robada, §5.0) — alien chico
stats: {vida: baja, dano: nulo, velocidad: alta, capacidad_robo: 1_recurso}
drops: [componente_comun (baja probabilidad)]
comportamiento_amanecer: huye con lo que cargue
notas_diseno: El enemigo tutorial. Enseña la regla central — te roban, no te matan — y con v0.2 enseña también la segunda mitad de la regla: robar lleva tiempo, y ese tiempo es tu oportunidad. Con D3 cerrada esa ventana es de 3-5 s, la misma para lo que sea que se lleve: el jugador aprende un solo ritmo.
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
tiempo_robo: default (3-5 s por cosa robada, §5.0) — alien chico
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
como_roba: Brazos elásticos que entran al refugio DESDE AFUERA — saquea por la ventana sin cruzar la puerta, así que los defensores de adentro no lo alcanzan. Tarda lo mismo que cualquiera (3-5 s), pero lo hace fuera del alcance de quien está adentro
contramedida: Eliminarlo a distancia, o una torre configurada con prioridad `ya_cargado` (§5.0) — es el enemigo que justifica esa opción
movimiento: terrestre
aparicion: noche 4+
tiempo_robo: default (3-5 s por cosa robada, §5.0)
stats: {vida: media, dano: nulo, velocidad: media, capacidad_robo: TBD}
drops: [componente_comun, componente_raro (baja)]
comportamiento_amanecer: huye con lo que cargue
notas_diseno: Su función era atacar la sensación de seguridad del muro; con D2 cerrada (no hay muros, ni siquiera como variante) pasa a atacar la sensación de seguridad del REFUGIO — el edificio deja de ser un búnker. La cláusula de barricadas se borró: ya no hay modo clásico que activar. Sigue en `propuesta` hasta que TASK-020 valide el mecanismo nuevo contra la regla de oro.
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
como_roba: OVNI pequeño con rayo tractor LENTO sobre vacas; de noche las vacas están guardadas en el establo (§5.3), así que tiene que sacarlas de ahí primero — 3-5 s por vaca, como cualquier otro robo. La lentitud da ventana de reacción
contramedida: Cualquier DPS aéreo básico (cazadores, torres)
movimiento: volador
aparicion: noche 3+
tiempo_robo: default (3-5 s por vaca, §5.0) — alien chico, se lleva una
stats: {vida: baja, dano: nulo, velocidad: baja, capacidad_robo: 1_vaca}
drops: [componente_comun, componente_antigrav (media)]
comportamiento_amanecer: huye con lo que cargue
notas_diseno: Primera imagen icónica del juego — la vaca flotando. Cómico Y amenazante. Enseña la mecánica de rescate por derribo. D3 cerrada resolvió su único hueco: el rayo tractor NO es instantáneo, tarda lo mismo que un robo a mano, así que el establo es defendible y la torre llega a tiempo.
estado: canon
```

### 2.2.2 platillo_abductor
```yaml
id: platillo_abductor
nombre: Platillo Abductor
tipo: enemigo
categoria: abductor
que_roba: personas
como_roba: Rayo tractor sobre unidades; se planta sobre el refugio y tarda 3-5 s en sacar a la persona antes de subirla. Escudo frontal — vulnerable por detrás
contramedida: Cazadores posicionados, arpón antigravedad (T3)
movimiento: volador
aparicion: noche 6+
tiempo_robo: default (3-5 s por aldeano, §5.0)
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
> Comportamiento base: no roba — ROMPE. Existía para destruir barricadas y abrir camino a los demás; **cerrada D2 no hay muros que romper, así que su blanco es lo que sí estorba: las torres colocadas y la estructura de los edificios-refugio.** Con D1 en variante A ese blanco deja de ser una interpretación: *todos* los aliens resuelven la torre que los engancha, y el tanque es el que lo hace bien. Romper un refugio no destruye lo que hay dentro: lo deja al descubierto y acelera el saqueo de los ladrones. Las tres fichas de esta categoría siguen en `propuesta` hasta que TASK-020 valide el blanco nuevo.

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
notas_diseno: Chequeo de progresión — si no has avanzado el árbol tecnológico, este enemigo te lo cobra. Sin muros su rol se afila como escudo móvil del grupo, y D1 (variante A) lo confirma: como las torres SÍ enganchan a los aliens, el Caparazón existe para comerse ese fuego mientras los ladrones pasan detrás. Sigue en `propuesta` hasta que TASK-020 lo valide, pero ya no por falta de decisión.
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
notas_diseno: Rompe el turtling. Su blanco ya era la torre, así que es el tanque que menos cambia con v0.2 — pero ahora que las torres son colocables donde el jugador quiera, castiga directamente el amontonarlas en un solo punto. Con D1 en variante A su rol se vuelve más nítido todavía: los demás aliens pelean la torre de cerca, él la borra desde fuera de rango. Sigue en `propuesta` junto con el resto de la categoría (TASK-020).
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
como_roba: Coloso que "cosecha" — arranca del suelo las torres colocadas y las usa como arma contra el resto de tus defensas
contramedida: TBD — pelea de jefe mid-game con fases
movimiento: terrestre
aparicion: evento mid-game (noche ~10, por definir)
tiempo_robo: n/a
stats: {vida: jefe, dano: muy_alto, velocidad: baja, capacidad_robo: 0}
drops: [componente_epico x2, nucleo_ganadero]
comportamiento_amanecer: huye (si sobrevive, vuelve la siguiente luna llena)
notas_diseno: Invierte la fantasía — el jugador es el ganado desde la perspectiva alien. Cerrada D2, la cláusula de barricadas se borró: su cosecha son las torres y nada más, que con D1 en variante A es justamente lo que el resto de la invasión ya estaba peleando. Diseño de fases pendiente; sigue en `propuesta` hasta TASK-020.
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
| placa_blindaje | Especial | Tanques | Blindaje de edificios-refugio y torres, munición perforante |
| cristal_psiquico | Especial | Psíquicos, hipnotizadores | Torre de Vigilancia mejorada, contramedidas mentales |
| cristal_lunar | Especial | Faro Lunar (garantizado) | Recetas exclusivas del ciclo lunar (TBD) |
| nucleo_asedio | Especial | Demoledor | Torre de largo alcance |
| herramienta_alien | Especial | Reparador | Reparación automática de torres y edificios |
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

**2. El rancho está abierto — y no hay variante con muros** (D2, cerrada). No
hay muros iniciales ni modo clásico opcional. La ficción lo explica: la invasión
es una sorpresa en un valle del oeste, no un asedio anunciado a un castillo;
nadie levantó una muralla porque nadie sabía que venía nadie. Los aliens
**se mueven, entran y disparan libremente**: nada les impide llegar. Lo que hay
entre ellos y el botín son dos cosas y ninguna es una pared —

- **el refugio**, que los obliga a entrar y a tardar (punto 3), y
- **las torres**, que les cobran esos segundos (punto 5).

Las personas, las vacas y los recursos **se refugian de noche** en los edificios
con `modo_noche: refugio` (o, si no hay uno cerca que los admita, en el
[`town_center`](#51-town_center), que es el refugio por defecto del rancho). La
[`barricada`](#58-barricada) queda **archivada**: se conserva como ficha
histórica, no como opción de partida.

**3. Robar cuesta tiempo, y ese tiempo es la ventana de defensa** (D3, cerrada).
El alien no "toca y desaparece": entra al **primer edificio-refugio que
encuentra en su camino** y se queda adentro cargando.

| Qué se lleva | Cuánto tarda |
|---|---|
| Un aldeano | **3–5 s** |
| Comida (o cualquier recurso) | **3–5 s** |
| Una vaca | **3–5 s** |

El valor exacto se **sortea dentro del rango una vez por oleada** (con el seed
del run, campo `tiempos_robo` de la ficha de oleada), no por robo: el jugador
aprende el ritmo de la noche y lo puede leer.

**Los aliens grandes se llevan dos cosas.** El tamaño del alien define su
capacidad y su velocidad:

| Tamaño | `capacidad_robo` | Tiempo |
|---|---|---|
| Chico | **1** cosa | 3–5 s |
| Grande | **2** cosas | 3–5 s × `multiplicador_grande` (**TBD** — pendiente de balance) |

Mientras carga es un blanco quieto. Si muere ahí dentro, **suelta lo que ya
tenía encima** y la víctima se libera viva (misma regla que el abductor
derribado, §2.2). Vaciar un refugio entero de gente es caro en segundos: ese es
el presupuesto que el jugador le pelea con torres.

> Qué enemigo cuenta como grande —y cuánto es `multiplicador_grande`— es trabajo
> de balance, no de esta regla: está anotado en el backlog de [§10](#10-backlog-de-fichas-pendientes).

**4. Cada edificio tiene su propio árbol de talentos** (D6, cerrada). Se abre
**clickeando el edificio**; lo que se compra ahí vale para *ese* edificio y para
ningún otro, ni siquiera para otro del mismo tipo. La estrategia del jugador es
qué árbol sube en qué edificio.

La primera bifurcación del árbol son las dos ramas canónicas, y son excluyentes:

- **`refugio_y_defensa`** — el edificio se arma: sigue guardando gente y además
  dispara a quien entre a robar.
- **`doble_refugio`** — el edificio no dispara, pero **duplica su capacidad**
  (más personas y más recursos adentro). Menos edificios que defender, más huevos
  en la misma canasta.

Dos graneros del mismo pueblo pueden ir por caminos distintos. El contenido del
árbol más allá de esa primera bifurcación, y sus costos, son `TBD`.

**5. Las torres se colocan donde el jugador quiera** (`slot: libre`) y se
configuran con una `prioridad_objetivo`:

| Prioridad | A quién dispara primero |
|---|---|
| `primero_en_llegar` | Al alien que entró primero al edificio que la torre cubre |
| `mas_cercano_a_recursos` | Al que está por alcanzar un refugio cargado |
| `ya_cargado` | Al que ya lleva algo encima — matarlo devuelve el botín |

**6. Los aliens atacan las torres primero — variante A** (D1, cerrada). Las
torres **no se ignoran**: el alien que entra en combate con una torre la
**resuelve antes** de seguir camino al edificio. La torre es un obstáculo, no un
espectador.

Consecuencias que heredan todas las fichas:

- **Colocar una torre es elegir dónde se pelea**, no solo a qué refugio cubrís.
  Una torre adelantada compra tiempo lejos del botín; una torre pegada al
  refugio pelea encima de la gente.
- **La torre es gastable.** Puede caer, y el reparador que la sostiene está
  afuera del refugio y es raptable (GDD §6.3).
- **El [`caparazon`](#232-caparazon) funciona como escudo móvil**: absorbe el
  fuego de las torres mientras los ladrones pasan detrás. Su lectura, que
  dependía de esta decisión, queda confirmada.
- `prioridad_objetivo` sigue siendo la decisión de configuración de la torre,
  pero ahora convive con el hecho de que la torre **recibe** daño.

> No se pidió que esto fuera configurable por dificultad ni por tipo de enemigo:
> **variante A es el comportamiento único** del juego. Si más adelante hace falta
> la palanca, es una decisión nueva, no un default que se pueda asumir.

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
notas_diseno: Puerta de entrada de la población, que es el recurso vivo y el que más roban (GDD §5.1). De noche es el edificio donde el robo por aldeano (3–5 s, §5.0) más se nota: una taberna llena tarda mucho en vaciarse, y esa demora es lo que le da sentido a poner torres cerca.
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
notas_diseno: El corral es el blanco del platillo_sonda — la vaca flotando es la imagen icónica del juego. Cuanto más ganado, más rápido se come el pasto (ver vaca y pasto en §7): el establo grande no es gratis, es una boca más grande. Guardar las vacas de noche las protege del abductor pero las concentra en un solo refugio robable; el nivel doble_refugio agranda esa apuesta. Con D3 cerrada el establo ES defendible: sacar cada vaca cuesta 3-5 s, igual que un aldeano, así que vaciar un corral lleno es caro en segundos y la torre llega.
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
notas_diseno: Sin científico el edificio no produce nada — raptarlo detiene la investigación (ver 1.6). Es el edificio cuyo valor depende de una unidad viva, y por eso el que peor tolera ser el refugio más cercano al flanco. También habilita las recetas del árbol tecnológico (GDD §8.1), que todavía no son fichas, y los árboles de talentos de los demás edificios (§5.0.4). D5 le dio su rol económico definitivo: la llegada del científico ABRE las mejoras, y todas se pagan con `pieza_alien` (§7.3), que se junta en el barrido del amanecer. Antes del científico las piezas se acumulan sin poder gastarse.
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
notas_diseno: Ya no vive en una línea de muros: se coloca libre, y decidir a qué edificio cubre es la decisión táctica del jugador. Matar a un ladrón mientras carga le hace soltar lo robado (§5.0.3), así que la torre le cobra al alien el tiempo que pasa adentro. Con D1 cerrada en variante A hace algo más: los aliens la atacan primero y la resuelven antes de seguir al refugio, así que colocarla también es elegir DÓNDE se pelea — y es gastable, porque puede caer. Su prioridad_objetivo es configurable por torre. Revela al sombrero_negro: sin torre, el infiltrado camina entre tu gente sin que las defensas lo lean como hostil. Recibe las armas de montaje torre del árbol tecnológico (GDD §8.1), que todavía no son fichas. Pasa a `canon`: lo único que la tenía en `propuesta` era D1, y D1 está cerrada — sus stats siguen `TBD` como los de todo el resto.
estado: canon
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
funcion: ARCHIVADA — línea defensiva por niveles del diseño anterior; el juego no tiene muros (D2, §5.0.2)
funcion_dia: n/a — no se construye
funcion_noche: n/a — no existe en partida
modo_noche: ninguno
capacidad_refugio: 0
prioridad_objetivo: n/a
slot: n/a
obtencion: n/a — no se obtiene. D2 descartó la variante de muros estilo Kingdom
desbloquea: n/a
niveles: n/a
stats: {vida: n/a, tiempo_construccion: n/a}
costo: {madera: n/a, chatarra: n/a}
notas_diseno: ARCHIVADA POR D2 (29 de agosto de 2026). Mato confirmó el rancho abierto sin muros iniciales y sin modo clásico opcional: no hay barricadas que construir ni que romper. La ficha se conserva entera como referencia histórica —explica por qué manos_largas, toro_de_marte y el_ganadero existen y contra qué se diseñaron— pero no se genera contenido a partir de ella ni se la usa en partida. El "muro" que el juego sí tendrá es el campo_fuerza_alien (5.9), que llega tarde y se paga con piezas alien. Los tres enemigos que colgaban de ella se rediseñan para el rancho abierto en TASK-020.
estado: archivada
```

### 5.9 campo_fuerza_alien
```yaml
id: campo_fuerza_alien
nombre: Campo de fuerza alien
tipo: edificio
funcion: Barrera de energía — ESTRUCTURA (D5). Es un desbloqueo post-científico que se paga con piezas alien
funcion_dia: Inactivo; el emisor recarga con tecnología alien
funcion_noche: Levanta una barrera de energía entre dos emisores; los aliens no la cruzan mientras aguante
modo_noche: defensa
capacidad_refugio: 0
prioridad_objetivo: n/a
slot: libre
obtencion: Desbloqueo — requiere el cientifico en el rancho (y por lo tanto el laboratorio) más X piezas alien juntadas en el barrido del amanecer (X = TBD, §7.3 y §8)
desbloquea: n/a
niveles: TBD
stats: {vida: TBD, tiempo_construccion: TBD, energia: TBD, tiempo_recarga: TBD}
costo: {pieza_alien: TBD, madera: TBD, chatarra: TBD}
notas_diseno: D5 CERRADA — es una estructura, no el arma T3 montable en torre. Cierra el arco irónico del juego: no levantás una muralla de madera, levantás la misma tecnología con la que te robaron, hecha con los restos de las naves que te vinieron a robar. Llega tarde por construcción y no por decreto: el científico llega por objetivo (§8) y recién entonces se abren las mejoras, que se pagan en piezas alien que solo se juntan barriendo restos de mañana (§7.3). Sigue en `propuesta` porque la ficha nunca se validó en prototipo (TASK-016), no porque falte una decisión. Todos sus valores son TBD — no se inventan.
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
tiempos_robo: {objeto_s: 3-5, multiplicador_grande: TBD}
determinista: true
notas_diseno: Plantilla, no balance. Existe para que el tipo oleada se ejercite de punta a punta en el pipeline mientras la curva real no está definida. Ninguna noche real debería referenciarla.
estado: propuesta
```

---

## 7. Recursos vivos y consumibles

> Tipo de ficha nuevo (`recurso`, §0). Existe porque la comida dejó de ser un
> número que sube solo: ahora es una cadena **pasto → vaca → comida**, y cada
> eslabón se puede cortar. La madera, que no tiene mecánica propia, sigue
> viviendo en GDD §5.1 como economía y no como ficha.
>
> Desde que se cerró **D5** hay un tercer recurso con mecánica propia: la
> **pieza alien** (§7.3), que se junta en el **barrido del amanecer** y es la
> moneda de todas las mejoras post-científico.

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
notas_diseno: FICHA NUEVA, sin validar — estaba pendiente en el backlog de la wiki desde v0.1. La vaca es la unidad de medida emocional del juego: es lo que se ve flotando en el rayo tractor y es lo que desbloquea gente (el científico llega cuando el rancho sostiene X vacas, GDD §6.4). El hambre le agrega la segunda forma de perderla: no te la roban, se te muere de a poco porque construiste mal. Si un abductor cargado cae, la vaca cae viva (§2.2). Con D3 cerrada, sacarla de un establo cuesta 3-5 s como cualquier otro robo: no se pierde antes de que la torre dispare. El X de "X vacas" NO se inventa acá: la curva de checkpoints ya está aprobada (D4, §8.1) y la vaca aparece en DOS de sus cuatro compuertas — C1 pide un rebaño chico sostenido, C4 uno grande bajo fuego. Los dos umbrales siguen pendientes de balance y salen del prototipo (§9.2).
estado: propuesta
```

### 7.3 pieza_alien
```yaml
id: pieza_alien
nombre: Pieza alien / Restos de nave
tipo: recurso
clase: consumible
fuente: Barrido del amanecer — tras defender la noche, la gente sale a recolectar comida Y a levantar los restos de las naves y los aliens caídos. Cuantos más derribás de noche, más piezas hay de mañana
consumo: Las mejoras post-científico. Sin cientifico en el rancho no hay en qué gastarlas: se acumulan
robable: si — es la chatarra/tecnología alien de GDD §5.1, y los ladrones se la llevan como cualquier recurso del refugio
funcion_dia: Se junta. El barrido del amanecer es la recompensa material de haber peleado bien la noche anterior
funcion_noche: Está guardada en el refugio (el laboratorio guarda las que no se investigaron) y es robable
stats: {produccion: TBD, consumo_por_unidad: TBD, capacidad: TBD}
notas_diseno: FICHA NUEVA (D5, 29 de agosto de 2026), sin validar. No es un recurso más: es el bucle que cierra la noche con el día. Matar aliens dejaba drops sueltos (§3); ahora deja además una cosecha, y salir a juntarla es lo primero que se hace de mañana, junto con la comida. Tres efectos de diseño: (1) la noche mala duele el doble, porque perdés gente Y no juntás piezas; (2) la noche bien peleada se paga sola; (3) el campo de fuerza y el resto de las mejoras cuestan piezas, así que el "muro" del late game se construye literalmente con los restos de quienes te vinieron a robar. Cuántas piezas cuesta cada mejora es TBD — no se inventa.
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
| `objetivo_cientifico` | **Última compuerta (C4)** de la curva de progresión (§8.1): sostener **X vacas vivas**, con las tres compuertas previas ya cumplidas. **La forma es canon** (Mato la aprobó el 29 de agosto de 2026); **X sigue `TBD`** — sale del prototipo, ver §9.2 | [`cientifico`](#16-cientifico) — y con él el `laboratorio` y **las mejoras**, que se pagan en [`pieza_alien`](#73-pieza_alien) | **forma canon** · valores `TBD` |
| `desbloqueo_campo_fuerza` | Tener el `cientifico` en el rancho **y** juntar **X piezas alien** (X = `TBD`) | [`campo_fuerza_alien`](#59-campo_fuerza_alien) | propuesta |
| `objetivo_sheriff` | `TBD` — candidato: sobrevivir N noches sin perder gente | [`sheriff`](#19-sheriff) | propuesta |
| `objetivo_doctor` | **La compuerta C2 `cp_poblacion_sostenida`** (§8.1): sostener población **y** no perder más de `P2_perdidas_max` personas en la ventana. **Confirmado por Mato** el 29 de agosto de 2026 — *"el Doctor se desbloquea en la compuerta 2, sí; es para que pueda sobrevivir hasta el final"*. Los valores siguen `TBD` (§9.2) | [`doctor`](#18-doctor) | **forma canon** · valores `TBD` |

- Un objetivo **no se compra**: se cumple jugando. Es la manera de que criar
  ganado o proteger gente sea progresión y no solo economía.
- **El científico es la bisagra del run** (D5): antes de él las piezas alien se
  acumulan sin uso; con él se abren las mejoras y recién ahí las piezas valen
  algo. Por eso su umbral no es un número suelto sino el final de una **curva de
  checkpoints** (§8.1), **aprobada por Mato** el 29 de agosto de 2026
  (`TASK-021`).
- Los objetivos todavía **no son un tipo de ficha**: viven en esta tabla hasta
  que haya suficientes como para que valga un esquema propio (§10).
- Ninguna condición numérica se inventa acá: las X son `TBD` hasta balance
  (regla 1 de §0).

### 8.1 Curva de progresión del científico — CANON (D4, aprobada por Mato)

> **Estado: la FORMA es canon** — Mato la aprobó el 29 de agosto de 2026
> (`TASK-021`, D4). Lo aprobado es la *forma*: cuatro compuertas, tres ejes, el
> `doctor` en C2 y el respiro post-luna-llena. **Ningún número de esta
> subsección está decidido**: los parámetros viven en §9.2, todos `TBD`, y se
> calibran en el prototipo (`TASK-010` / `TASK-005`).

**Cuatro compuertas ordenadas, tres ejes distintos, el científico al final** —
no un umbral único de vacas. Cada compuerta se evalúa **al amanecer** (en el
barrido, §7.3), abre algo visible y premia un comportamiento que las otras no
premian: **construir** (ganado), **defender gente** (población) y **matar**
(piezas alien). Un solo eje se optimiza y se rompe; tres en secuencia obligan a
jugar el juego entero antes de la bisagra.

| # | id | Eje | Condición (parametrizada) | Abre |
|---|---|---|---|---|
| **C1** | `cp_ganado_inicial` | Ganado sostenido (bajo) | `vacas_vivas >= P1_vacas` sostenido `P1_amaneceres` amaneceres consecutivos | **La curva se vuelve visible**: el aviso del profesor aparece en el [`town_center`](#51-town_center) con el tablón de las cuatro compuertas |
| **C2** | `cp_poblacion_sostenida` | Población sostenida | `poblacion_viva >= P2_poblacion` **y** `personas_robadas <= P2_perdidas_max` en las últimas `P2_ventana` noches | El [`doctor`](#18-doctor) — **confirmado por Mato**: es el `objetivo_doctor` de §8, y llega acá para que el jugador *pueda sobrevivir hasta el final* |
| **C3** | `cp_piezas_barrido` | Piezas alien acumuladas | `piezas_alien_recolectadas_acumuladas >= P3_piezas` (acumulado del run, **no** stock actual) | El **barrido del amanecer rinde más**: el rancho desmonta naves grandes y alcanza los restos lejanos ([`pieza_alien`](#73-pieza_alien)) |
| **C4** | `objetivo_cientifico` | Ganado sostenido (alto) | `vacas_vivas >= P4_vacas` sostenido `P4_amaneceres` amaneceres consecutivos, **con C1–C3 cumplidas** | El [`cientifico`](#16-cientifico) → [`laboratorio`](#55-laboratorio), árboles de talento (§5.0.4) y **todas las mejoras** post-científico (D5) |

**Por qué C4 vuelve al eje de C1.** No es repetición: C1 pregunta *¿sabés
criar?*, C4 pregunta *¿podés sostenerlo bajo fuego?*. La frase de Mato queda
intacta —el científico **sí** llega por vacas—; lo que se agrega es lo que hay
que haber hecho antes de que ese número cuente.

**Ejes descartados**, y por qué:

- **Noches sobrevividas** — no entra como compuerta: es un temporizador
  disfrazado, se cumple solo y premia esconderse. Entra en **un** rol
  subordinado: como **unidad de medida** del "sostenido" (se cuenta en
  amaneceres consecutivos). El techo de piedad por número de noches que se le
  había propuesto a Mato **quedó descartado**: la piedad existe, pero colgada
  del ciclo lunar y no de un contador de noches (§8.2).
- **Recursos acumulados** (madera, comida en depósito) — mide paciencia, se
  farmea sin riesgo y ya está implícito: sin economía no se llega a `P4_vacas`.
- **Aliens derribados** — se solapa con C3 y premia farmear spawns baratos. Las
  piezas cuentan lo mismo *y* exigen sobrevivir hasta la mañana para juntarlas.
- **Nivel de pueblo / renombre** — es justo lo que v0.2 sacó del juego.
- **Cualquier eje del héroe** — rompe coop (regla 7): las cuatro condiciones son
  del **rancho**, no de un jugador.

**Pedir piezas antes del científico no es circular, es el punto.** Las piezas se
**juntan** desde la noche 1 (D5); el científico habilita **gastarlas**. C3 le da
lectura al único tramo muerto del diseño: mientras no tenés en qué gastarlas,
cuentan para traer a quien te deja gastarlas.

**Cómo la ve el jugador** (alimenta el aviso previo de `TASK-017`): un **tablón**
en el `town_center` con las cuatro compuertas —la cumplida tachada, la actual con
barra y número, las futuras con título visible y cifra en gris—; se **resuelve al
amanecer**, nunca en mitad de la noche; avisa cuando falta poco (`P_aviso`) **y
cuando retrocedés** por un robo. Una compuerta cumplida **no se pierde**; lo que
se reinicia es la ventana de sostenimiento de la compuerta en curso.

**Riesgo anotado:** las mejoras y los árboles de talento cuelgan del
`laboratorio`, o sea de C4, así que C1–C3 dan poco poder tangible. Por eso C2 da
una unidad y C3 una capacidad económica. Si hiciera falta más peso en el early,
la palanca es mover una mejora barata a pre-científico — y eso **sí** sería
tocar D5.

### 8.2 El respiro post-luna-llena — la piedad, decidida por Mato

> **Decisión de Mato, 29 de agosto de 2026** (`TASK-021`, D4): *"darles 2 o 3
> noches suaves después de la luna llena para que se recuperen, como Kingdom"*.
> La forma es canon; las magnitudes son `TBD` (§9.2).

**La piedad va ON, pero no como techo.** Al equipo se le había ocurrido un
*techo de piedad* —pasadas N noches, la curva se relaja sola y el científico
llega igual—, y esa forma **queda descartada**: rescataba al jugador atascado
por reloj y le sacaba sentido a las cuatro compuertas. Lo que entra en su lugar
es otra cosa, y no toca la curva:

**Tras cada luna llena, las `P_respiro_noches` noches siguientes son más
suaves** — menos intensidad de oleada (`P_respiro_intensidad`), para que el
rancho se recupere del pico antes de que el escalado siga subiendo.

- **Cuelga del ciclo lunar, no de un contador de noches.** El ancla es la luna
  llena (GDD §9), que ya está telegrafiada con días de anticipación. No hay
  condición oculta ni rescate silencioso: el jugador ve venir el examen *y* ve
  venir el descanso.
- **No relaja ninguna compuerta.** C1–C4 se cumplen igual, con los mismos
  umbrales. El respiro cambia la **presión de las oleadas**, no la curva: si el
  jugador está atascado, le da noches para rehacer el rebaño y repoblar la
  taberna, no le regala el científico.
- **Por qué esta forma y no la otra:** el juego castiga en espiral a propósito
  (regla 3 del proyecto), y una espiral sin valle no se sale nunca. El respiro
  le da al jugador el tramo en el que la espiral se puede revertir **jugando**;
  el techo de piedad se la revertía sin jugar.
- **Referencia declarada:** *Kingdom*. El ciclo de sangre y calma es el ritmo
  que Mato quiere — pico, respiro, pico más alto.
- **Coop-ready:** es una propiedad de la noche, no de un jugador. Con 1 o 2
  héroes el respiro es el mismo.
- **Consume:** el sistema de oleadas (§6) y el ciclo lunar de GDD §9. El
  modificador lunar de la ficha de oleada ya es el lugar donde vive este valor;
  lo que agrega esta decisión es que el modificador de las noches
  inmediatamente posteriores a la llena es **menor que el de una noche
  estándar**, no igual.

---

## 9. Decisiones registradas (y lo que sigue abierto)

> Las seis preguntas que dejó el cambio de mecánica. **Las seis están cerradas
> al 29 de agosto de 2026**: cinco se respondieron directo y la sexta (D4) pasó
> por una fase de balance —`TASK-021` propuso la curva, Mato la aprobó ese mismo
> día—. Cada ficha que dependía de una la sigue referenciando por su `Dn`, ahora
> como decisión y no como pendiente. **No queda ninguna decisión abierta**; lo
> que queda es calibración numérica, y esa es del prototipo (§9.2).

### 9.1 Decisiones cerradas

| # | Decisión de Mato | Qué cambió | Dónde quedó registrada |
|---|---|---|---|
| **D1** ✅ | **Variante A: los aliens atacan las torres primero.** No las ignoran — resuelven la torre que los engancha antes de llegar a los edificios. No se pidió que fuera configurable: variante A es el comportamiento único | La torre es un obstáculo y es gastable; colocarla es elegir *dónde se pelea*, no solo a qué refugio cubrís. El `caparazon` como escudo móvil queda confirmado | [§5.0](#50-reglas-de-los-edificios-de-noche-cambio-canónico) punto 6, [`torre_vigilancia`](#56-torre_vigilancia) (→ `canon`), [`caparazon`](#232-caparazon), [`demoledor`](#233-demoledor), §2.3 |
| **D2** ✅ | **Sin muros, y sin variante clásica.** No hay muros iniciales ni modo *Kingdom* opcional. Los aliens se mueven, entran y disparan libremente; la defensa es **refugio + torres**. Gente, vacas y recursos se refugian en los edificios que los admiten o en el `town_center` | La [`barricada`](#58-barricada) pasa a `archivada`. Los tres enemigos diseñados contra ella se rediseñan para el rancho abierto: no hay barricadas que romper | §5.0 punto 2, [`barricada`](#58-barricada), [`manos_largas`](#213-manos_largas), [`toro_de_marte`](#231-toro_de_marte), [`el_ganadero`](#252-el_ganadero) |
| **D3** ✅ | **3–5 s por cosa robada, aleatorio** — aldeano, comida o vaca, el mismo rango para las tres. **Los aliens grandes se llevan DOS cosas y tardan más** (multiplicador `TBD`) | **Revisa el 1–3 s / 2 s anterior**, que ya no rige. El establo es defendible: la vaca no se pierde antes de que la torre dispare | §5.0 punto 3, esquema de oleada (§0), [`oleada_ejemplo`](#61-oleada_ejemplo), [`platillo_sonda`](#221-platillo_sonda), [`platillo_abductor`](#222-platillo_abductor), [`ratero_gris`](#211-ratero_gris), [`coyote_plateado`](#212-coyote_plateado), [`establo`](#53-establo), [`vaca`](#72-vaca) |
| **D4** ✅ | **La curva de progresión del científico, aprobada** (29/08/2026, `TASK-021`). Tres respuestas: (1) **la forma va** — cuatro compuertas sobre tres ejes (C1 sobrevivencia/ganado, C2 comunidad/población, C3 capacidad económica/piezas), con el científico en C4; (2) **el `doctor` se desbloquea en C2**, *"es para que pueda sobrevivir hasta el final"*; (3) **la piedad va ON en una forma concreta**: tras la luna llena, **2–3 noches suaves** para recuperarse, *"como Kingdom"* — **no** el techo de piedad por número de noches que se le había propuesto | La curva deja de ser propuesta y pasa a ser la forma canónica de la progresión. `objetivo_doctor` deja de ser `TBD`: es `cp_poblacion_sostenida`. Aparece el **respiro post-luna-llena** como mecánica del ciclo lunar. **Los once parámetros siguen `TBD`**: lo aprobado es la forma, los números salen del prototipo (§9.2) | [§8.1](#81-curva-de-progresión-del-científico--canon-d4-aprobada-por-mato), [§8.2](#82-el-respiro-post-luna-llena--la-piedad-decidida-por-mato), §8 (`objetivo_cientifico`, `objetivo_doctor`), §9.2 (parámetros), [`cientifico`](#16-cientifico), [`doctor`](#18-doctor), [`vaca`](#72-vaca) |
| **D5** ✅ | **El campo de fuerza es una estructura y un desbloqueo post-científico.** Cuando llega el científico se abren las mejoras; las mejoras se pagan con **X piezas alien**. Mecánica nueva: **de mañana, tras defender de noche, la gente sale a recolectar comida Y piezas de las naves alien caídas** | Ficha nueva [`pieza_alien`](#73-pieza_alien) (§7.3) y el **barrido del amanecer** como parte del día. El "muro" del late game se construye con los restos de quienes te vinieron a robar | §7.3, [`campo_fuerza_alien`](#59-campo_fuerza_alien), [`laboratorio`](#55-laboratorio), §8 (`desbloqueo_campo_fuerza`) |
| **D6** ✅ | **Árbol de talentos POR EDIFICIO.** Se abre **clickeando el edificio**; lo que comprás vale para ese edificio y para ningún otro, ni del mismo tipo. No hay árbol global | La progresión deja de ser una compra por tipo y pasa a ser la estrategia de layout del jugador. La bifurcación `refugio_y_defensa` / `doble_refugio` es la primera rama de ese árbol | §5.0 punto 4, esquema de edificio (§0), todas las fichas de §5 |

### 9.2 D4 — la forma está aprobada, los números son del prototipo

| # | Estado | Qué decidió Mato |
|---|---|---|
| **D4** ✅ | **Forma aprobada** (`TASK-021`, 29/08/2026) · **valores `TBD`** | Mato no eligió un número de vacas a ciegas: pidió una fase de balance, el equipo propuso la curva y él la **aprobó en tres puntos** — (1) **la forma**: cuatro compuertas sobre tres ejes (sobrevivencia, comunidad, capacidad económica); (2) el **`doctor` en C2**; (3) la **piedad ON** como respiro post-luna-llena de 2–3 noches suaves (§8.2), descartando el techo por número de noches |

**Lo aprobado es la forma, no los valores** (regla 5 del proyecto). La curva
canónica vive en [§8.1](#81-curva-de-progresión-del-científico--canon-d4-aprobada-por-mato):
cuatro compuertas (`cp_ganado_inicial` → `cp_poblacion_sostenida` →
`cp_piezas_barrido` → `objetivo_cientifico`) sobre tres ejes —ganado sostenido,
población sostenida y piezas alien—, con *noches sobrevividas* descartada como
compuerta. El respiro post-luna-llena está en
[§8.2](#82-el-respiro-post-luna-llena--la-piedad-decidida-por-mato).

**Lo que sigue pendiente son estos parámetros, todos `TBD`.** El rango es de
arranque para el prototipo, **no un valor aprobado** — se calibra en `TASK-010` /
`TASK-005` con el juego andando:

| Parámetro | Unidad | Valor | Rango de arranque (sin aprobar) |
|---|---|---|---|
| `P1_vacas` | vacas vivas | `TBD` | 2–4 |
| `P1_amaneceres` | amaneceres consecutivos | `TBD` | 1–2 |
| `P2_poblacion` | aldeanos vivos en el rancho | `TBD` | 5–8 (atado a `taberna.capacidad_refugio`, `TBD`) |
| `P2_perdidas_max` | personas robadas en la ventana | `TBD` | 0–1 |
| `P2_ventana` | noches (ventana móvil) | `TBD` | 2–3 |
| `P3_piezas` | piezas alien acumuladas en el run | `TBD` | el barrido de 2–4 noches bien defendidas — **relativo**, porque `pieza_alien.produccion` es `TBD` |
| `P4_vacas` | vacas vivas | `TBD` | 8–14 (≈ 3–4 × `P1_vacas`); debe exigir granja extra, el pasto es el freno (§7.1) |
| `P4_amaneceres` | amaneceres consecutivos | `TBD` | 2–4 — el parámetro más sensible de la curva |
| `P_aviso` | distancia al objetivo para avisar | `TBD` | falta ≤1 unidad, o ≤20–25 % |
| `P_respiro_noches` | noches suaves después de cada luna llena | `TBD` | **2–3 — rango fijado por Mato** (§8.2), no de arranque; el valor exacto dentro del rango sale del prototipo |
| `P_respiro_intensidad` | intensidad de oleada en esas noches | `TBD` | por debajo de una noche estándar del mismo tramo — **cuánto**, sin rango: depende de la curva de oleadas (`TASK-008`) |
| `N_objetivo` | noche en la que llega el científico jugando bien | `TBD` | 6–10 — **el único número que importa calibrar**; los otros son medios para caer en esta ventana |

**Las tres preguntas que `TASK-021` le hizo a Mato, y sus respuestas
(29/08/2026):** (1) *¿cuatro compuertas y estos tres ejes?* → **sí, la forma se
aprueba** tal cual, con los ejes leídos como sobrevivencia (C1), comunidad (C2)
y capacidad económica (C3). (2) *¿el `doctor` como recompensa de C2?* → **sí**,
*"es para que pueda sobrevivir hasta el final"*. (3) *¿techo de piedad OFF u
ON?* → **ON, pero en otra forma**: no un techo por número de noches, sino
**2–3 noches suaves después de la luna llena**, *"como Kingdom"* (§8.2).

**Los números no se contestaron, y era lo correcto:** salen del prototipo
apuntando a `N_objetivo` (noches 6–10).

### 9.3 Cómo se cierra una decisión

Cuando una decisión se cierra: se escribe acá el resultado, se actualizan las
fichas que la referencian, recién ahí el GDD resume el cambio, y por último se
destraban los tickets que la esperaban.

---

## 10. Backlog de fichas pendientes
- [ ] Armas del árbol tecnológico como fichas (T1/T2/T3) con costos en componentes — §4 solo cubre las armas ya referenciadas por `arma_base`
- [ ] Curva de oleadas real: presupuesto por noche × modificador lunar, y el costo en puntos como campo de la ficha de enemigo (TECH §3.3)
- [x] Ganado como entidad → `vaca` (§7.2), con la cadena del `pasto` (§7.1). Faltan variantes de ganado, si las hay
- [ ] Variantes de luna llena de cada enemigo (sufijo `_lunar`: stats modificados)
- [ ] Valores de balance de todos los `TBD` (tras prototipo)
- [ ] Reconciliar los cinco enemigos que quedaron en `propuesta` (`manos_largas`, `toro_de_marte`, `caparazon`, `demoledor`, `el_ganadero`) con el rancho abierto de §5.0 — **destrabado**: D1 y D2 están cerradas, lo hace `TASK-020`
- [ ] Clasificar cada enemigo que roba como **chico o grande** (`capacidad_robo` 1 o 2) y fijar el `multiplicador_grande` de §5.0 punto 3 — es balance, no diseño (D3 fijó la regla, no el reparto)
- [ ] Fichas de objetivo/desbloqueo (GDD §6.4): "X vacas → llega el científico" y "científico + X piezas → campo de fuerza" hoy son prosa en §8, no entidades
- [ ] Costo en `pieza_alien` de cada mejora post-científico — depende de la curva de progresión de `TASK-021`
- [ ] Magnitud de los bonus de las tres clases de héroe (§11) y cómo se apilan en coop — es balance puro, `TASK-023` lo deja parametrizado
- [ ] Héroes concretos dentro de cada clase (§11): hoy la clase es el arquetipo y el héroe es genérico. Los héroes desbloqueables entre runs son fichas que todavía no existen (`TASK-024`)

---

## 11. Clases del héroe

> **Decisión de Mato, 29 de agosto de 2026.** El personaje que controlás
> ([GDD §4](GDD.md#4-controles-y-personaje)) deja de ser un ranchero genérico:
> al empezar la run elegís **una de tres clases**, y cada clase mejora **un solo
> eje** del rancho. No es una unidad de §1 —esas se reclutan—, es el jugador.

**La regla de las clases:** una clase = un eje. El Sheriff no toca la economía,
el Alcalde no dispara mejor, el Carpintero no sube el daño. Elegir clase es
elegir **qué parte de la espiral del robo** ([§5.0](#50-reglas-de-los-edificios-de-noche-cambio-canónico))
peleás mejor: matarlos antes (ataque), reponer más rápido lo que te sacaron
(economía) o que te saquen menos y te quepa más adentro (defensa y capacidad).

- **Coop-ready:** cada héroe elige su clase por separado y los bonus se aplican
  sobre el mismo rancho compartido ([GDD §4.2](GDD.md#42-cooperativo-local-definido)).
  Dos jugadores pueden traer la misma clase; cómo se apilan los bonus repetidos
  es `TBD` de balance.
- **Entre runs** las clases son el marco de la meta-progresión
  ([GDD §8.3](GDD.md#83-meta-progresión-entre-runs)): los puntos de fin de run
  se gastan en **mejorar** la clase que jugás o en **desbloquear héroes nuevos**
  que pertenecen a una de las tres. Las tres clases son el eje fijo; los héroes,
  el contenido que crece.
- **Ningún número está decidido.** `magnitud_bonus` y `escalado_por_nivel` son
  `TBD` en las tres fichas (regla 1 de [§0](#0-instrucciones-para-sistemas-de-ia)).

### 11.1 hero_clase_sheriff
```yaml
id: hero_clase_sheriff
nombre: Sheriff
tipo: clase_heroe
bonus: ataque
alcance: El daño de tus edificios (torres y edificios con modo_noche defensa) y el de tus unidades del jugador (§1)
funcion_dia: Sin efecto económico propio — el Sheriff no produce, prepara la noche
funcion_noche: La ventana de robo (§5.0) se cierra antes porque todo lo tuyo pega más fuerte: el alien muere cargado y suelta el botín
stats: {magnitud_bonus: TBD, escalado_por_nivel: TBD}
meta_progresion: Los puntos de fin de run suben el bonus de ataque y desbloquean héroes de esta clase (GDD §8.3)
notas_diseno: La clase de "matarlos antes de que terminen de sacar". No cambia la economía ni la capacidad: si te desbordan, te desbordan igual. Ojo con el nombre — la unidad reclutable `sheriff` (§1.9) es otra cosa y sigue existiendo; si conviven en pantalla hay que desambiguar la ficción (¿el héroe Sheriff hace redundante al NPC Sheriff?), y eso es diseño pendiente, no balance.
estado: propuesta
```

### 11.2 hero_clase_alcalde
```yaml
id: hero_clase_alcalde
nombre: Alcalde
tipo: clase_heroe
bonus: economia
alcance: La producción de todos tus recursos — comida de las granjas, madera, chatarra, la cadena del ganado (§7) y el barrido del amanecer (§7.3)
funcion_dia: El día rinde más: más producción por edificio y más rendimiento del barrido del amanecer
funcion_noche: Sin efecto de combate propio — lo que aporta es la reposición del día siguiente
stats: {magnitud_bonus: TBD, escalado_por_nivel: TBD}
meta_progresion: Los puntos de fin de run suben el bonus de economía y desbloquean héroes de esta clase (GDD §8.3)
notas_diseno: La clase que pelea la espiral del robo por el otro lado: no evita que te roben, hace que reponerlo cueste menos noches. Es la que más se nota en runs largas y la que peor la pasa si te desarman temprano. Riesgo de balance a vigilar: si el bonus toca las piezas alien (§7.3) acelera el desbloqueo del científico, que es la bisagra del run (D5/D4) — si eso desbalancea la curva de `TASK-021`, el alcance se recorta.
estado: propuesta
```

### 11.3 hero_clase_carpintero
```yaml
id: hero_clase_carpintero
nombre: Carpintero
tipo: clase_heroe
bonus: defensa_capacidad
alcance: La defensa de tus recursos (vida de los edificios y cuánto tarda un alien en sacarles algo) y la capacidad_refugio de todos tus edificios
funcion_dia: Los edificios aguantan más y guardan más: sube el techo de gente, ganado y recursos que entran de noche
funcion_noche: Alarga la ventana de robo (§5.0) — el alien tarda más adentro y tus torres tienen más tiempo de matarlo cargado
stats: {magnitud_bonus: TBD, escalado_por_nivel: TBD}
meta_progresion: Los puntos de fin de run suben el bonus de defensa/capacidad y desbloquean héroes de esta clase (GDD §8.3)
notas_diseno: La clase que compra segundos, que es la moneda real del juego desde v0.4. Toca los dos números que definen el rancho abierto: cuánto entra al refugio y cuánto tarda el alien en sacarlo. Es la clase más acoplada a §5.0, así que cualquier cambio de la ventana de robo la revisa. En coop se lee natural que uno traiga Carpintero y otro Sheriff: uno estira la ventana, el otro la aprovecha.
estado: propuesta
```

---

*Wiki v0.2 — 9 unidades, 16 enemigos, 5 armas, 9 edificios (1 archivada), 1 oleada, 3 recursos, 3 clases de héroe, 10 componentes. Fuente canónica: cambios de diseño se hacen aquí primero y se resumen en el GDD.*
