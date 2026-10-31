# Adivinator

Juego de adivinanzas al estilo *Akinator* construido sobre un **árbol binario de decisión**.

- Cada **nodo interno** guarda una pregunta; su rama **SÍ** (derecha) y su rama **NO** (izquierda) llevan a otra pregunta o a un personaje.
- Cada **hoja** guarda un personaje.
- Cuando Adivinator falla, la hoja se convierte en una nueva pregunta con dos hijos: el personaje viejo y el nuevo. Así el árbol **crece con cada partida** y se guarda en `data/arbol.json`.

## Estructura

```
adivinator/
  tree.py      # Nodo y ArbolDecision (recorrido, aprendizaje, serialización)
  storage.py   # Persistencia del árbol en JSON (thread-safe)
  app.py       # Aplicación Flask (application factory)
index.py       # Entrypoint para flask / gunicorn
templates/     # Vistas Jinja2
static/        # CSS e imágenes
tests/         # pytest
```

La raíz del árbol nunca cambia: el progreso de cada partida se guarda en la
sesión como un *camino* (lista de respuestas `si`/`no`) desde la raíz.

## Ejecutar

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
flask --app index run --debug      # http://localhost:5000
pytest
```

Variables de entorno opcionales: `SECRET_KEY` (firma de la sesión) y
`ARBOL_PATH` (ruta del JSON del árbol).

En producción: `gunicorn index:app` (ver `Procfile`).
