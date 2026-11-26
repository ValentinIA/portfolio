"""Insignias (badges) para tecnologías, estados y categorías.

Devuelven texto Markdown con la sintaxis de Streamlit `:color-badge[texto]`,
para poder combinar varias insignias en una sola línea con st.markdown.
"""

from collections.abc import Iterable

from core.modelos import EstadoProyecto

_COLOR_ESTADO = {
    EstadoProyecto.FUNCIONAL: "green",
    EstadoProyecto.PROTOTIPO: "blue",
    EstadoProyecto.PRUEBA_DE_CONCEPTO: "violet",
    EstadoProyecto.PENDIENTE: "gray",
}


def _insignia(texto: str, color: str) -> str:
    # Los corchetes cerrarían la directiva antes de tiempo: se escapan.
    texto = texto.replace("[", r"\[").replace("]", r"\]")
    return f":{color}-badge[{texto}]"


def insignias(textos: Iterable[str], color: str = "gray") -> str:
    return " ".join(_insignia(t, color) for t in textos)


def insignia_estado(estado: EstadoProyecto) -> str:
    return _insignia(estado.etiqueta, _COLOR_ESTADO[estado])
