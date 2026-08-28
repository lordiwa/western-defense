---
title: Inicio
permalink: /
description: >-
  Western Defense — tower defense Weird West de scroll lateral. Documentación
  viva: diseño, wiki canónica de entidades y documento técnico.
---

<div class="hero" markdown="1">

# Western Defense

<p class="tagline">Un tower defense del Viejo Oeste donde los alienígenas no vienen a matarte.<br>Vienen a <strong>robarte</strong>.</p>

</div>

De día explorás el desierto y gestionás tu rancho. De noche caen los platillos y
se llevan lo que puedan: gente, ganado, chatarra, tecnología. Cada cosa que te
roban te deja más débil para el día siguiente. No hay un *game over* de golpe —
hay una espiral. Y de los enemigos caídos sacás su tecnología para armarte
mejor, hasta poder marchar contra la nave nodriza y liberar el valle.

*1870s, Weird West, cómic pulp. Gracioso en la superficie, inquietante en lo que
no te termina de explicar.*

## Por dónde empezar

<div class="cards" markdown="0">

  <a class="card" href="{{ '/GDD.html' | relative_url }}">
    <h3>Diseño del juego (GDD)</h3>
    <p>La visión completa: el core loop día/noche, la economía, el rancho, la
    progresión, el ciclo lunar y el tono. <strong>Empezá por acá</strong> si es
    tu primera vez.</p>
  </a>

  <a class="card" href="{{ '/wiki/' | relative_url }}">
    <h3>Wiki de entidades — índice</h3>
    <p>Tablas navegables de todo lo que existe en el juego: unidades, enemigos,
    armas, edificios y oleadas. La forma más rápida de ver el catálogo entero.</p>
  </a>

  <a class="card" href="{{ '/WIKI.html' | relative_url }}">
    <h3>Fichas completas</h3>
    <p>El documento canónico entero, ficha por ficha, con todos los campos.
    39 fichas. Lo que dice acá es lo que vale.</p>
  </a>

  <a class="card" href="{{ '/TECH.html' | relative_url }}">
    <h3>Documento técnico</h3>
    <p>Arquitectura, stack (Godot 4 + C#), plan de implementación y cómo la wiki
    se convierte en datos del juego. Para cuando toque programar.</p>
  </a>

</div>

## Cómo funciona esta documentación

Tres documentos, cada uno con un trabajo:

| Documento | Responde |
|---|---|
| [**GDD**]({{ '/GDD.html' | relative_url }}) | *¿Qué es este juego y por qué es divertido?* Diseño, mecánicas, tono. |
| [**Wiki**]({{ '/wiki/' | relative_url }}) | *¿Qué cosas existen exactamente?* Cada unidad, enemigo, arma y edificio. |
| [**Técnico**]({{ '/TECH.html' | relative_url }}) | *¿Cómo se construye?* Arquitectura, stack, orden de trabajo. |

Dos cosas que conviene saber antes de leer la wiki:

- **La wiki manda.** No es un resumen del juego: es la definición. Los datos del
  juego se *generan* desde estas fichas. Si la wiki y el código no coinciden, el
  que está mal es el código.
- **`TBD` significa "todavía no decidido".** Los números de balance marcados así
  están deliberadamente en blanco. Nadie los inventa: se llenan probando.
  Ahora mismo hay **110 campos TBD** repartidos en las fichas, y 19 fichas en
  estado `propuesta` (o sea, escritas pero sin validar en prototipo).

## La regla que ordena todo el diseño

> **Todo enemigo quiere llevarse algo.**
> Si aparece un enemigo nuevo, tiene que contestar tres preguntas: *¿qué roba?*,
> *¿cómo lo roba?* y *¿cómo se lo evitás?* Un enemigo que solo hace daño no
> entra en este juego.

Y su corolario: **el robo duele más que la muerte**. Los enemigos no destruyen
tu rancho, te lo vacían. Perder es quedarte sin nada con qué defenderte mañana.

## Para el que quiera opinar

Todo esto vive en el repositorio y se puede comentar ahí:

- [Repositorio en GitHub]({{ site.repo_url }}) — el proyecto entero.
- [Abrir un issue]({{ site.repo_url }}/issues/new) — la forma más simple de
  dejar una duda, una idea o un "esto no se entiende". No hace falta saber
  programar.
- [Preguntas abiertas del GDD]({{ '/GDD.html#13-preguntas-abiertas-para-v04' | relative_url }})
  — las decisiones que todavía están en el aire. Buen lugar para meter mano.
