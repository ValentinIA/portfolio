"""Página sobre mí: perfil, idiomas, experiencia, formación y cursos."""

import streamlit as st

from components.insignias import insignias
from components.trayectoria import entrada_experiencia, entrada_formacion
from servicios.contenido import obtener_perfil, obtener_trayectoria

perfil = obtener_perfil()
trayectoria = obtener_trayectoria()

st.title("Sobre mí", anchor=False)

# --- Perfil (izquierda) e idiomas (derecha) ----------------------------------

col_perfil, col_idiomas = st.columns([3, 2], gap="large")

with col_perfil:
    st.caption(f":material/location_on: {perfil.ubicacion}")
    st.markdown(perfil.presentacion)
    if perfil.aprendiendo:
        st.caption(f":material/school: Aprendiendo ahora: {perfil.aprendiendo}")

with col_idiomas:
    st.header("Idiomas", anchor=False)
    st.markdown(insignias(f"{i.idioma} · {i.nivel}" for i in trayectoria.idiomas))

# --- Experiencia · Cursos · Formación en una sola fila ----------------------
# Tres columnas en lugar de secciones apiladas: la altura total es la de la
# columna más alta, así la página cabe en una pantalla sin hacer scroll.

col_experiencia, col_cursos, col_formacion = st.columns(3, gap="medium")

with col_experiencia:
    st.header("Experiencia", anchor=False)
    for experiencia in trayectoria.experiencia:
        entrada_experiencia(experiencia)

with col_cursos:
    st.header("Cursos", anchor=False)
    for curso in trayectoria.cursos:
        entrada_formacion(curso)

with col_formacion:
    st.header("Formación", anchor=False)
    for formacion in trayectoria.formacion:
        entrada_formacion(formacion)
