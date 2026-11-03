"""Árbol binario de decisión que sostiene el juego Adivinator.

Cada nodo interno guarda una pregunta; su rama ``no`` (izquierda) y su rama
``si`` (derecha) llevan a más preguntas o a una hoja. Cada hoja guarda el
nombre de un personaje.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterator, Literal, Optional

Respuesta = Literal["si", "no"]
RESPUESTAS: tuple[Respuesta, ...] = ("si", "no")


@dataclass
class Nodo:
    data: str
    left: Optional["Nodo"] = None   # rama "no"
    right: Optional["Nodo"] = None  # rama "si"

    def es_hoja(self) -> bool:
        return self.left is None and self.right is None

    def hijo(self, respuesta: Respuesta) -> Optional["Nodo"]:
        return self.right if respuesta == "si" else self.left

    def to_dict(self) -> dict:
        if self.es_hoja():
            return {"personaje": self.data}
        return {
            "pregunta": self.data,
            "si": self.right.to_dict() if self.right else None,
            "no": self.left.to_dict() if self.left else None,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Nodo":
        if "personaje" in data:
            return cls(data["personaje"])
        return cls(
            data["pregunta"],
            left=cls.from_dict(data["no"]) if data.get("no") else None,
            right=cls.from_dict(data["si"]) if data.get("si") else None,
        )


class ArbolDecision:
    """Árbol binario cuya raíz nunca cambia; se recorre mediante caminos.

    Un *camino* es una secuencia de respuestas (``"si"`` / ``"no"``) desde la
    raíz. Guardar el camino en lugar de un puntero al nodo permite que el
    estado de cada partida viva fuera del árbol (por ejemplo en la sesión web)
    sin modificar la estructura compartida.
    """

    def __init__(self, raiz: Nodo) -> None:
        self.raiz = raiz

    # ----- Recorrido --------------------------------------------------------
    def nodo_en(self, camino: list[str]) -> Nodo:
        nodo = self.raiz
        for respuesta in camino:
            if respuesta not in RESPUESTAS:
                raise ValueError(f"Respuesta inválida: {respuesta!r}")
            siguiente = nodo.hijo(respuesta)
            if siguiente is None:
                raise ValueError("El camino se sale del árbol")
            nodo = siguiente
        return nodo

    def recorrer(self) -> Iterator[Nodo]:
        """Recorrido en preorden (útil para depurar e inspeccionar)."""
        pila = [self.raiz]
        while pila:
            nodo = pila.pop()
            yield nodo
            if nodo.right:
                pila.append(nodo.right)
            if nodo.left:
                pila.append(nodo.left)

    def personajes(self) -> list[str]:
        return [n.data for n in self.recorrer() if n.es_hoja()]

    def altura(self) -> int:
        def _altura(nodo: Optional[Nodo]) -> int:
            if nodo is None:
                return 0
            return 1 + max(_altura(nodo.left), _altura(nodo.right))

        return _altura(self.raiz)

    # ----- Crecimiento ------------------------------------------------------
    def aprender(
        self,
        camino: list[str],
        personaje: str,
        pregunta: str,
        respuesta_nuevo: Respuesta,
    ) -> None:
        """Reemplaza la hoja en ``camino`` por una pregunta que distingue al
        personaje adivinado (viejo) del personaje nuevo.

        ``respuesta_nuevo`` es la respuesta a ``pregunta`` que corresponde al
        personaje nuevo; el personaje viejo queda en la rama opuesta.
        """
        if respuesta_nuevo not in RESPUESTAS:
            raise ValueError(f"Respuesta inválida: {respuesta_nuevo!r}")
        personaje, pregunta = personaje.strip(), pregunta.strip()
        if not personaje or not pregunta:
            raise ValueError("El personaje y la pregunta no pueden estar vacíos")

        hoja = self.nodo_en(camino)
        if not hoja.es_hoja():
            raise ValueError("Sólo se puede aprender a partir de una hoja")

        viejo = Nodo(hoja.data)
        nuevo = Nodo(personaje)
        # La hoja se convierte en pregunta: así el árbol crece in situ sin
        # tocar la raíz ni el camino que llevó hasta aquí.
        hoja.data = pregunta
        if respuesta_nuevo == "si":
            hoja.right, hoja.left = nuevo, viejo
        else:
            hoja.right, hoja.left = viejo, nuevo

    # ----- Serialización ----------------------------------------------------
    def to_dict(self) -> dict:
        return self.raiz.to_dict()

    @classmethod
    def from_dict(cls, data: dict) -> "ArbolDecision":
        return cls(Nodo.from_dict(data))
