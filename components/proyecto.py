"""Componentes de proyecto: tarjeta (Inicio y listado) y enlaces externos."""

import streamlit as st

from components.enlaces import enlace_recurso
from components.insignias import insignia_estado, insignias
from core.modelos import Proyecto

PAGINA_PROYECTOS = "app_pages/proyectos.py"


def cabecera_insignias(proyecto: Proyecto) -> None:
    st.markdown(f"{insignia_estado(proyecto.estado)} {insignias([proyecto.categoria], 'blue')}")


def enlaces_externos(proyecto: Proyecto) -> None:
    """Enlaces al código, la documentación y la demo, solo si existen."""
    enlaces = [
        ("Código", proyecto.repo_url, ":material/code:"),
        ("Documentación", proyecto.docs_url, ":material/description:"),
        ("Demo", proyecto.demo_url, ":material/play_circle:"),
    ]
    for etiqueta, recurso, icono in enlaces:
        if recurso:
            enlace_recurso(etiqueta, recurso, icono)


def tarjeta_proyecto(proyecto: Proyecto) -> None:
    with st.container(border=True, height="stretch"):
        cabecera_insignias(proyecto)
        st.subheader(proyecto.titulo, anchor=False)
        st.markdown(proyecto.resumen)
        st.markdown(insignias(proyecto.tecnologias))
        st.space("stretch")
        with st.container(horizontal=True, vertical_alignment="center"):
            st.page_link(
                PAGINA_PROYECTOS,
                label="Ver detalle",
                icon=":material/arrow_forward:",
                query_params={"p": proyecto.slug},
            )
            enlaces_externos(proyecto)
