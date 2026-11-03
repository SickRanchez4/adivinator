import json

import pytest

from adivinator import create_app


@pytest.fixture
def client(tmp_path):
    app = create_app({"TESTING": True, "ARBOL_PATH": str(tmp_path / "arbol.json"), "SECRET_KEY": "test"})
    return app.test_client()


def jugar(client, respuestas):
    client.post("/jugar/iniciar")
    for r in respuestas:
        client.post("/jugar/responder", data={"respuesta": r})
    return client.get("/jugar")


def test_inicio_crea_arbol_inicial(client, tmp_path):
    assert client.get("/").status_code == 200
    assert (tmp_path / "arbol.json").exists()


def test_flujo_acierto(client):
    r = jugar(client, ["si"])
    assert "Perro" in r.get_data(as_text=True)
    r = client.post("/jugar/acierto")
    assert "Adivinator gana" in r.get_data(as_text=True)


def test_flujo_fallo_aprende_y_persiste(client, tmp_path):
    jugar(client, ["si"])
    r = client.get("/jugar/fallo")
    assert "Perro" in r.get_data(as_text=True)

    r = client.post(
        "/jugar/aprender",
        data={"personaje": "Gato", "pregunta": "¿Maúlla?", "respuesta_nuevo": "si"},
    )
    assert "Aprendido" in r.get_data(as_text=True)

    datos = json.loads((tmp_path / "arbol.json").read_text(encoding="utf-8"))
    assert datos["si"]["pregunta"] == "¿Maúlla?"
    assert datos["si"]["si"]["personaje"] == "Gato"
    assert datos["si"]["no"]["personaje"] == "Perro"

    # La siguiente partida ya recorre el nuevo camino
    r = jugar(client, ["si", "si"])
    assert "Gato" in r.get_data(as_text=True)


def test_aprender_con_datos_invalidos_redirige_con_error(client):
    jugar(client, ["si"])
    r = client.post(
        "/jugar/aprender",
        data={"personaje": "", "pregunta": "¿Maúlla?", "respuesta_nuevo": "si"},
        follow_redirects=True,
    )
    assert "no pueden estar vacíos" in r.get_data(as_text=True)


def test_sin_partida_devuelve_400(client):
    assert client.get("/jugar").status_code == 400
    assert client.post("/jugar/responder", data={"respuesta": "si"}).status_code == 400


def test_pagina_arbol(client):
    r = client.get("/arbol")
    assert r.status_code == 200
    assert "Perro" in r.get_data(as_text=True) and "Messi" in r.get_data(as_text=True)
