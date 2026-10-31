"""Aplicación web Flask para Adivinator."""

from __future__ import annotations

import os
from pathlib import Path

from flask import (
    Flask,
    abort,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from .storage import RepositorioArbol
from .tree import RESPUESTAS

BASE_DIR = Path(__file__).resolve().parent.parent


def create_app(config: dict | None = None) -> Flask:
    app = Flask(
        __name__,
        template_folder=str(BASE_DIR / "templates"),
        static_folder=str(BASE_DIR / "static"),
    )
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY", "dev-cambiar-en-produccion"),
        ARBOL_PATH=os.environ.get("ARBOL_PATH", str(BASE_DIR / "data" / "arbol.json")),
    )
    if config:
        app.config.update(config)

    repositorio = RepositorioArbol(Path(app.config["ARBOL_PATH"]))
    app.extensions["repositorio"] = repositorio

    # ----- Helpers ----------------------------------------------------------
    def camino_actual() -> list[str]:
        camino = session.get("camino")
        if camino is None:
            abort(400, "No hay una partida en curso")
        return camino

    def nodo_actual():
        try:
            return repositorio.arbol.nodo_en(camino_actual())
        except ValueError:
            # El árbol cambió (otra partida aprendió algo); reiniciamos.
            session.pop("camino", None)
            abort(409, "La partida quedó desactualizada, empieza de nuevo")

    # ----- Rutas ------------------------------------------------------------
    @app.get("/")
    def inicio():
        return render_template("home.html", total=len(repositorio.arbol.personajes()))

    @app.get("/about")
    def about():
        return render_template("about.html")

    @app.get("/arbol")
    def ver_arbol():
        arbol = repositorio.arbol
        return render_template(
            "arbol.html",
            raiz=arbol.raiz,
            altura=arbol.altura(),
            personajes=arbol.personajes(),
            nuevo=session.pop("ultimo_aprendido", None),
        )

    @app.post("/jugar/iniciar")
    def iniciar():
        session["camino"] = []
        return redirect(url_for("jugar"))

    @app.get("/jugar")
    def jugar():
        nodo = nodo_actual()
        plantilla = "adivinanza.html" if nodo.es_hoja() else "pregunta.html"
        return render_template(plantilla, nodo=nodo)

    @app.post("/jugar/responder")
    def responder():
        respuesta = request.form.get("respuesta")
        if respuesta not in RESPUESTAS:
            abort(400, "Respuesta inválida")
        nodo = nodo_actual()
        if nodo.es_hoja():
            abort(400, "Ya se llegó a un personaje")
        camino = camino_actual() + [respuesta]
        session["camino"] = camino
        return redirect(url_for("jugar"))

    @app.post("/jugar/acierto")
    def acierto():
        nodo = nodo_actual()
        session.pop("camino", None)
        return render_template("resultado.html", gano_maquina=True, personaje=nodo.data)

    @app.get("/jugar/fallo")
    def fallo():
        nodo = nodo_actual()
        if not nodo.es_hoja():
            abort(400)
        return render_template("aprender.html", personaje_viejo=nodo.data)

    @app.post("/jugar/aprender")
    def aprender():
        camino = camino_actual()
        personaje = request.form.get("personaje", "")
        pregunta = request.form.get("pregunta", "")
        respuesta_nuevo = request.form.get("respuesta_nuevo", "")
        try:
            repositorio.aprender(camino, personaje, pregunta, respuesta_nuevo)
        except ValueError as exc:
            flash(str(exc), "error")
            return redirect(url_for("fallo"))
        session.pop("camino", None)
        session["ultimo_aprendido"] = personaje.strip()
        return render_template(
            "resultado.html", gano_maquina=False, personaje=personaje.strip()
        )

    return app
