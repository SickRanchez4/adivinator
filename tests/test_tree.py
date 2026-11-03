import pytest

from adivinator.tree import ArbolDecision, Nodo


@pytest.fixture
def arbol():
    return ArbolDecision(Nodo("¿Es un animal?", right=Nodo("Perro"), left=Nodo("Messi")))


def test_nodo_en_recorre_el_camino(arbol):
    assert arbol.nodo_en([]).data == "¿Es un animal?"
    assert arbol.nodo_en(["si"]).data == "Perro"
    assert arbol.nodo_en(["no"]).data == "Messi"


def test_nodo_en_rechaza_caminos_invalidos(arbol):
    with pytest.raises(ValueError):
        arbol.nodo_en(["si", "si"])
    with pytest.raises(ValueError):
        arbol.nodo_en(["quizas"])


def test_aprender_convierte_hoja_en_pregunta_sin_mover_la_raiz(arbol):
    raiz = arbol.raiz
    arbol.aprender(["si"], "Gato", "¿Maúlla?", "si")

    assert arbol.raiz is raiz
    nodo = arbol.nodo_en(["si"])
    assert nodo.data == "¿Maúlla?"
    assert nodo.right.data == "Gato"
    assert nodo.left.data == "Perro"
    assert arbol.nodo_en(["si", "si"]).data == "Gato"


def test_aprender_respeta_la_rama_no(arbol):
    arbol.aprender(["si"], "Pez", "¿Ladra?", "no")
    assert arbol.nodo_en(["si", "si"]).data == "Perro"
    assert arbol.nodo_en(["si", "no"]).data == "Pez"


def test_aprender_valida_entrada(arbol):
    with pytest.raises(ValueError):
        arbol.aprender([], "Gato", "¿Maúlla?", "si")  # la raíz no es hoja
    with pytest.raises(ValueError):
        arbol.aprender(["si"], "  ", "¿Maúlla?", "si")
    with pytest.raises(ValueError):
        arbol.aprender(["si"], "Gato", "¿Maúlla?", "tal vez")


def test_el_arbol_crece_indefinidamente(arbol):
    camino = ["si"]
    for i in range(20):
        arbol.aprender(camino, f"Animal{i}", f"¿Pregunta {i}?", "si")
        camino = camino + ["si"]
    assert arbol.nodo_en(camino).data == "Animal19"
    assert len(arbol.personajes()) == 22
    assert arbol.altura() == 22


def test_serializacion_ida_y_vuelta(arbol):
    arbol.aprender(["si"], "Gato", "¿Maúlla?", "si")
    copia = ArbolDecision.from_dict(arbol.to_dict())
    assert copia.to_dict() == arbol.to_dict()
    assert copia.personajes() == arbol.personajes()
