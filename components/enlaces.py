"""Enlaces: botones de perfiles profesionales y enlaces a recursos (PDFs, repos...)."""

import streamlit as st

from core.cargador import es_url
from core.modelos import Enlace

# Streamlit publica la carpeta static/ en esta ruta (server.enableStaticServing).
# Es relativa: funciona igual en local y en Streamlit Cloud.
PREFIJO_STATIC = "app/static/"


def url_publica(recurso: str) -> str:
    """Convierte un recurso del contenido en una URL que el navegador puede abrir."""
    return recurso if es_url(recurso) else PREFIJO_STATIC + recurso


def enlace_recurso(etiqueta: str, recurso: str, icono: str) -> None:
    """Enlace discreto (sin borde) que abre el recurso en una pestaña nueva."""
    st.link_button(etiqueta, url_publica(recurso), icon=icono, type="tertiary")


def botones_enlaces(enlaces: tuple[Enlace, ...], cv: str | None = None) -> None:
    if cv:
        st.link_button("Ver CV", url_publica(cv), icon=":material/description:")
    for enlace in enlaces:
        st.link_button(enlace.nombre, enlace.url, icon=":material/open_in_new:")
