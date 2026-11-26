"""Botones de enlaces profesionales (GitHub, LinkedIn...), usados en Inicio y Contacto."""

import streamlit as st

from core.modelos import Enlace


def botones_enlaces(enlaces: tuple[Enlace, ...]) -> None:
    for enlace in enlaces:
        st.link_button(enlace.nombre, enlace.url, icon=":material/open_in_new:")
