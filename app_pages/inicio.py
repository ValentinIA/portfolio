"""Página de inicio: presentación profesional, proyecto destacado y tecnologías."""

import streamlit as st

from components.enlaces import botones_enlaces
from components.insignias import insignias
from components.proyecto import tarjeta_proyecto
from servicios.contenido import obtener_perfil, obtener_proyecto_destacado

perfil = obtener_perfil()
destacado = obtener_proyecto_destacado()

# --- Presentación (izquierda) y proyecto destacado (derecha) -----------------
# En pantallas estrechas (≤ 640 px) las columnas se apilan automáticamente.

col_presentacion, col_destacado = st.columns([3, 2], gap="large")

with col_presentacion:
    st.title(perfil.nombre, anchor=False)
    st.subheader(perfil.titular, anchor=False)
    st.caption(f":material/location_on: {perfil.ubicacion}")
    st.markdown(perfil.presentacion)
    st.markdown(insignias(perfil.orientacion, "blue"))

    with st.container(horizontal=True):
        if st.button(
            "Ver proyectos",
            type="primary",
            icon=":material/folder_open:",
            key="inicio_ver_proyectos",
        ):
            st.switch_page("app_pages/proyectos.py")
        botones_enlaces(perfil.enlaces, perfil.cv)

with col_destacado:
    if destacado:
        st.header("Proyecto destacado", anchor=False)
        tarjeta_proyecto(destacado)

# --- Tecnologías (ancho completo) --------------------------------------------

st.header("Tecnologías", anchor=False)
with st.grid("auto", min_column_width=220):
    for grupo in perfil.competencias:
        with st.container(border=True, height="stretch"):
            st.markdown(f"**{grupo.nombre}**")
            st.markdown(insignias(grupo.tecnologias))
