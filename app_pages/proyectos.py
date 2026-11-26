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
    # --- Vista de detalle -----------------------------------------------------
    st.page_link(PAGINA_PROYECTOS, label="Todos los proyectos", icon=":material/arrow_back:")
    st.title(proyecto.titulo, anchor=False)
    cabecera_insignias(proyecto)
    st.markdown(proyecto.resumen)
    with st.container(horizontal=True):
        enlaces_externos(proyecto)

    st.markdown(obtener_detalle_proyecto(proyecto.slug))

    st.subheader("Tecnologías", anchor=False)
    st.markdown(insignias(proyecto.tecnologias))

else:
    # --- Vista de listado -----------------------------------------------------
    if slug:
        st.warning("El proyecto que buscas no existe. Estos son todos los disponibles.")

    st.title("Proyectos", anchor=False)
    st.caption("Cada proyecto indica su estado: funcional, prototipo o prueba de concepto.")

    with st.grid("auto", min_column_width=300):
        for p in obtener_proyectos():
            tarjeta_proyecto(p)
