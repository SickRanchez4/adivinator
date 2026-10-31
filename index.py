"""Punto de entrada: ``flask --app index run`` o ``gunicorn index:app``."""

from adivinator import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
