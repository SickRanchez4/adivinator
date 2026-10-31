"""Persistencia del árbol en un archivo JSON.

Así el conocimiento acumulado sobrevive a reinicios del servidor y el árbol
sigue creciendo partida tras partida.
"""

from __future__ import annotations

import json
import threading
from pathlib import Path

from .tree import ArbolDecision, Nodo

ARBOL_INICIAL = ArbolDecision(
    Nodo(
        "¿Es un animal?",
        right=Nodo("Perro"),
        left=Nodo("Messi"),
    )
)


class RepositorioArbol:
    """Carga y guarda un ``ArbolDecision`` de forma segura entre hilos."""

    def __init__(self, ruta: Path) -> None:
        self.ruta = Path(ruta)
        self._lock = threading.Lock()
        self._arbol: ArbolDecision | None = None

    @property
    def arbol(self) -> ArbolDecision:
        if self._arbol is None:
            self._arbol = self._cargar()
        return self._arbol

    def _cargar(self) -> ArbolDecision:
        if self.ruta.exists():
            with self.ruta.open(encoding="utf-8") as f:
                return ArbolDecision.from_dict(json.load(f))
        arbol = ArbolDecision.from_dict(ARBOL_INICIAL.to_dict())
        self._escribir(arbol)
        return arbol

    def _escribir(self, arbol: ArbolDecision) -> None:
        self.ruta.parent.mkdir(parents=True, exist_ok=True)
        tmp = self.ruta.with_suffix(".tmp")
        with tmp.open("w", encoding="utf-8") as f:
            json.dump(arbol.to_dict(), f, ensure_ascii=False, indent=2)
        tmp.replace(self.ruta)

    def aprender(self, camino: list[str], personaje: str, pregunta: str, respuesta_nuevo: str) -> None:
        with self._lock:
            self.arbol.aprender(camino, personaje, pregunta, respuesta_nuevo)  # type: ignore[arg-type]
            self._escribir(self.arbol)
