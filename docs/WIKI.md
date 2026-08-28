# COWBOY DEFENSE — Wiki de Entidades v0.1

> **Propósito:** Fuente canónica de todas las entidades del juego (unidades del jugador, enemigos, edificios, armas). Este documento está estructurado para ser **consumido por sistemas de IA** que generen la wiki pública, assets, código de datos (ScriptableObjects / Resources) o contenido de balance.
> **Documentos hermanos:** [`GDD.md`](GDD.md) (diseño general) · [`TECH.md`](TECH.md) (técnico)
> **Navegación:** [índice de la wiki](wiki/README.md) — tablas por categoría con enlaces a cada ficha (generado, no editar a mano).

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
stats: {vida: TBD, dano: TBD, velocidad: TBD, capacidad_robo: TBD}
drops:         # componentes que suelta al morir + rareza
comportamiento_amanecer: huye con lo que cargue  # default
notas_diseno:
estado:
```

---

## 1. Unidades del Jugador

### 1.1 peon
```yaml
id: peon
nombre: Peón
tipo: unidad_jugador
rol: economico
obtencion: Recluta base en la Taberna
funcion_dia: Recolecta madera y chatarra, construye edificios
funcion_noche: Repara barricadas (riesgo de rapto), se refugia si no hay órdenes
arma_base: ninguna
raptable: true
stats: {vida: TBD, dano: 0, cadencia: n/a, rango: n/a, velocidad: TBD}
costo: {madera: 0, chatarra: 0, comida_upkeep: TBD}
mejoras: [carretilla (más carga), herramientas (construye más rápido)]
notas_diseno: La sangre del pueblo y el objetivo favorito de los Ladrones. Su pérdida frena toda la economía.
estado: canon
```

### 1.2 pistolero
```yaml
id: pistolero
nombre: Pistolero
tipo: unidad_jugador
rol: defensivo
obtencion: Peón + revólver fabricado en la Armería
funcion_dia: Escolta a recolectores fuera de las murallas
funcion_noche: Defensa a distancia en las barricadas
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
funcion_dia: Pastorea ganado, aumenta producción de comida
funcion_noche: Protege el corral; puede enlazar con lazo
arma_base: lazo
raptable: true
stats: {vida: TBD, dano: bajo, cadencia: TBD, rango: corto, velocidad: TBD}
costo: {madera: 0, chatarra: TBD, comida_upkeep: TBD}
mejoras: [lazo reforzado]
notas_diseno: Mecánica a validar en prototipo — el lazo puede jalar de vuelta ganado siendo abducido o inmovilizar aliens pequeños.
estado: propuesta
```

### 1.6 cientifico
```yaml
id: cientifico
nombre: Científico / Profesor
tipo: unidad_jugador
rol: investigacion
obtencion: Llega al pueblo al alcanzar cierto nivel/renombre, o se encuentra explorando
funcion_dia: Investiga tecnología alien en el Laboratorio; desbloquea recetas del árbol tecnológico
funcion_noche: Se refugia (no pelea)
arma_base: ninguna
raptable: true
stats: {vida: baja, dano: 0, cadencia: n/a, rango: n/a, velocidad: baja}
costo: {madera: 0, chatarra: 0, comida_upkeep: TBD}
mejoras: [asistente (segunda cola de investigación)]
notas_diseno: Si te lo raptan, la investigación se DETIENE. Es la unidad más valiosa y más frágil — protegerlo es una decisión de layout.
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

## 2.1 Categoría: LADRON
> Comportamiento base: entra por un flanco, corre al objetivo robable más cercano, toma y huye por donde vino. Frágil, veloz, en grupo.

### 2.1.1 ratero_gris
```yaml
id: ratero_gris
nombre: Ratero Gris
tipo: enemigo
categoria: ladron
que_roba: recursos
como_roba: Corre al depósito o recurso suelto más cercano, carga lo que puede y huye
contramedida: Cualquier defensa lo mata; el reto es el volumen del grupo
movimiento: terrestre
aparicion: noche 1+
stats: {vida: baja, dano: nulo, velocidad: alta, capacidad_robo: 1_recurso}
drops: [componente_comun (baja probabilidad)]
comportamiento_amanecer: huye con lo que cargue
notas_diseno: El enemigo tutorial. Enseña la regla central — te roban, no te matan.
estado: canon
```

### 2.1.2 coyote_plateado
```yaml
id: coyote_plateado
nombre: Coyote Plateado
tipo: enemigo
categoria: ladron
que_roba: comida
como_roba: Muy rápido, esquiva en zigzag; prioriza granjas y almacén de comida
contramedida: Escopetas (área) y trampas; las balas simples fallan por su esquiva
movimiento: terrestre
aparicion: noche 2+
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
como_roba: Brazos elásticos que roban POR ENCIMA de barricadas bajas sin romperlas
contramedida: Muros altos (mejora de barricada) o eliminarlo a distancia antes de que llegue
movimiento: terrestre
aparicion: noche 4+
stats: {vida: media, dano: nulo, velocidad: media, capacidad_robo: TBD}
drops: [componente_comun, componente_raro (baja)]
comportamiento_amanecer: huye con lo que cargue
notas_diseno: Ataca la sensación de seguridad del muro. Empuja la mejora vertical de defensas.
estado: canon
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
como_roba: OVNI pequeño con rayo tractor LENTO sobre vacas; la lentitud da ventana de reacción
contramedida: Cualquier DPS aéreo básico (cazadores, torres)
movimiento: volador
aparicion: noche 3+
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
como_roba: Rayo tractor sobre unidades; escudo frontal — vulnerable por detrás
contramedida: Cazadores posicionados, arpón antigravedad (T3)
movimiento: volador
aparicion: noche 6+
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
stats: {vida: media, dano: nulo, velocidad: baja, capacidad_robo: 1_persona}
drops: [componente_raro]
comportamiento_amanecer: huye con lo que cargue
notas_diseno: El enemigo de terror del juego. No es fuerte — es que no lo VES. Justifica la existencia de la Torre de Vigilancia y crea paranoia ("¿ese es de los nuestros?").
estado: canon
```

## 2.3 Categoría: TANQUE
> Comportamiento base: no roba — ROMPE. Existe para destruir barricadas y abrir camino a los demás.

### 2.3.1 toro_de_marte
```yaml
id: toro_de_marte
nombre: Toro de Marte
tipo: enemigo
categoria: tanque
que_roba: nada (rompe)
como_roba: n/a — embiste barricadas con carga telegrafiada
contramedida: Daño concentrado durante el telegraph; dinamita
movimiento: terrestre
aparicion: noche 5+
stats: {vida: alta, dano: alto_vs_estructuras, velocidad: baja_con_cargas, capacidad_robo: 0}
drops: [componente_raro, placa_blindaje]
comportamiento_amanecer: huye
notas_diseno: Espejo alienígena del ganado que te roban — un toro, pero suyo. Primera amenaza real a los muros.
estado: canon
```

### 2.3.2 caparazon
```yaml
id: caparazon
nombre: Caparazón
tipo: enemigo
categoria: tanque
que_roba: nada (rompe)
como_roba: n/a — avanza lento con blindaje frontal total, golpea estructuras
contramedida: Flanqueo, daño en área, armas de plasma T3 (ignoran armadura)
movimiento: terrestre
aparicion: noche 8+
stats: {vida: muy_alta, dano: medio_vs_estructuras, velocidad: muy_baja, capacidad_robo: 0}
drops: [placa_blindaje, componente_raro]
comportamiento_amanecer: huye
notas_diseno: Chequeo de progresión — si no has avanzado el árbol tecnológico, este enemigo te lo cobra.
estado: canon
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
stats: {vida: media, dano: alto_vs_torres, velocidad: baja, capacidad_robo: 0}
drops: [componente_raro, nucleo_asedio]
comportamiento_amanecer: huye
notas_diseno: Rompe el turtling — no puedes solo esconderte tras los muros; obliga a salidas nocturnas.
estado: canon
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
como_roba: Rayo tractor masivo capaz de levantar varias víctimas; llega con escolta de abductores y soporte
contramedida: Concentrar antiaéreo; derribarla suelta TODO lo que cargue
movimiento: volador
aparicion: lunas llenas (mini-jefe recurrente)
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
como_roba: Coloso que "cosecha": arranca barricadas del suelo y las usa como arma contra tus torres
contramedida: TBD — pelea de jefe mid-game con fases
movimiento: terrestre
aparicion: evento mid-game (noche ~10, por definir)
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

## 4. Backlog de fichas pendientes
- [ ] Edificios como fichas (town_center, taberna, establo, armeria, laboratorio, torre_vigilancia, granja, barricada) — mismo esquema, campos de niveles de mejora
- [ ] Armas del árbol tecnológico como fichas (T1/T2/T3) con costos en componentes
- [ ] Ganado como entidad (vaca: produce comida, raptable, ¿variantes?)
- [ ] Variantes de luna llena de cada enemigo (sufijo `_lunar`: stats modificados)
- [ ] Valores de balance de todos los `TBD` (tras prototipo)

---

*Wiki v0.1 — 9 unidades, 16 enemigos, 10 componentes. Fuente canónica: cambios de diseño se hacen aquí primero y se resumen en el GDD.*
