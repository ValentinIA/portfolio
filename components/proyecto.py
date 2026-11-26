"""Tarjeta de proyecto, reutilizada en Inicio (destacado) y en el listado de Proyectos."""

import streamlit as st

from components.insignias import insignia_estado, insignias
from core.modelos import Proyecto


def tarjeta_proyecto(proyecto: Proyecto) -> None:
    with st.container(border=True, height="stretch"):
        st.markdown(f"{insignia_estado(proyecto.estado)} {insignias([proyecto.categoria], 'blue')}")
        st.subheader(proyecto.titulo, anchor=False)
        st.markdown(proyecto.resumen)
        st.markdown(insignias(proyecto.tecnologias))
        st.space("stretch")
        with st.container(horizontal=True, vertical_alignment="center"):
            st.page_link(
                "app_pages/proyectos.py",
                label="Ver detalle",
                icon=":material/arrow_forward:",
                query_params={"p": proyecto.slug},
            )
            if proyecto.repo_url:
                st.page_link(proyecto.repo_url, label="Código", icon=":material/code:")
