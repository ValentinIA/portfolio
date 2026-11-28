"""Página de proyectos: listado y vista de detalle.

La URL decide qué vista se muestra:
- /proyectos               -> listado de tarjetas
- /proyectos?p=<slug>      -> detalle de ese proyecto (URL compartible)
"""

import streamlit as st

from components.insignias import insignias
from components.proyecto import (
    PAGINA_PROYECTOS,
    cabecera_insignias,
    enlaces_externos,
    tarjeta_proyecto,
)
from servicios.contenido import buscar_proyecto, obtener_detalle_proyecto, obtener_proyectos

slug = st.query_params.get("p")
proyecto = buscar_proyecto(slug)

if proyecto:
    # --- Vista de detalle: texto a la izquierda, ficha a la derecha ----------
    st.page_link(PAGINA_PROYECTOS, label="Todos los proyectos", icon=":material/arrow_back:")
    st.title(proyecto.titulo, anchor=False)

    col_detalle, col_ficha = st.columns([2, 1], gap="large")

    with col_detalle:
        st.markdown(proyecto.resumen)
        st.markdown(obtener_detalle_proyecto(proyecto.slug))

    with col_ficha, st.container(border=True):
        cabecera_insignias(proyecto)
        st.subheader("Tecnologías", anchor=False)
        st.markdown(insignias(proyecto.tecnologias))
        enlaces_externos(proyecto)

else:
    # --- Vista de listado -----------------------------------------------------
    if slug:
        st.warning("El proyecto que buscas no existe. Estos son todos los disponibles.")

    st.title("Proyectos", anchor=False)
    st.caption("Cada proyecto indica su estado: funcional, prototipo o prueba de concepto.")

    with st.grid("auto", min_column_width=320):
        for p in obtener_proyectos():
            tarjeta_proyecto(p)
