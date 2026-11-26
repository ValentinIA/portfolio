"""Página de inicio: presentación profesional, tecnologías y proyecto destacado."""

import streamlit as st

from components.enlaces import botones_enlaces
from components.insignias import insignias
from components.proyecto import tarjeta_proyecto
from servicios.contenido import obtener_perfil, obtener_proyecto_destacado

perfil = obtener_perfil()

# --- Presentación -------------------------------------------------------------

st.title(perfil.nombre, anchor=False)
st.subheader(perfil.titular, anchor=False)
st.caption(f":material/location_on: {perfil.ubicacion}")
st.markdown(perfil.presentacion)
st.markdown(insignias(perfil.orientacion, "blue"))

with st.container(horizontal=True):
    if st.button(
        "Ver proyectos", type="primary", icon=":material/folder_open:", key="inicio_ver_proyectos"
    ):
        st.switch_page("app_pages/proyectos.py")
    botones_enlaces(perfil.enlaces)

# --- Proyecto destacado -------------------------------------------------------

destacado = obtener_proyecto_destacado()
if destacado:
    st.header("Proyecto destacado", divider="gray")
    tarjeta_proyecto(destacado)

# --- Tecnologías --------------------------------------------------------------

st.header("Tecnologías", divider="gray")
with st.grid("auto", min_column_width=240):
    for grupo in perfil.competencias:
        with st.container(border=True, height="stretch"):
            st.markdown(f"**{grupo.nombre}**")
            st.markdown(insignias(grupo.tecnologias))
