# Backlog local (hivemind)

Fuente de tickets del equipo agéntico mientras no haya Jira. Un archivo JSON
por tarea, con nombres de campo compatibles con Jira para poder migrar 1:1.

## Layout

```
tasks/
├── README.md        ← este archivo
├── schema.json      ← JSON Schema de una tarea
├── index.json       ← índice regenerable: key → title/status/priority
└── TASK-001.json    ← un archivo por tarea
```

## Convenciones

- **Un JSON por tarea**, nombrado `<key>.json` (`TASK-001.json`).
- **Claves secuenciales**, tres dígitos, prefijo `TASK-`. Al crear una nueva,
  incrementá la más alta.
- **Fechas ISO-8601 UTC** (`2026-08-28T00:00:00Z`).
- **`index.json` es regenerable** — derivalo de los archivos por tarea; que no
  quede desincronizado.

## Ciclo de vida

```
todo → in_progress → in_review → done
              ↘ blocked ↗
```

El orquestador transiciona el estado; developer y reviewer agregan comentarios
y enlazan commits/PRs.

## Ejes del backlog inicial

| Etiqueta | Qué agrupa |
|---|---|
| `docs` | GDD, TECH, wiki: contenido y consistencia |
| `wiki` | Fichas canónicas de entidades |
| `balance` | Valores `TBD` y curvas |
| `pipeline` | `tools/wiki_to_resources.py` y la generación de `data/` |
| `godot` | Proyecto, escenas, C# |
| `prototipo` | Entregables de las 6 semanas de TECH §4 |
| `riesgo` | Los riesgos técnicos de TECH §6 |

## Reglas del proyecto que aplican a todo ticket

1. La wiki (`docs/WIKI.md`) es la **fuente canónica**: los datos y el código se
   derivan de ahí.
2. **Nunca inventar valores `TBD`.** Si un ticket pide proponer balance, la
   ficha se marca `estado: propuesta` y se justifica.
3. Todo enemigo **quiere llevarse algo**: qué roba, cómo lo roba, cómo se evita.
4. **Coop-ready siempre**: ningún sistema asume un jugador en singular.
