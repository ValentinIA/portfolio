"""Página sobre mí: perfil, experiencia, formación e idiomas."""

import streamlit as st

from components.insignias import insignias
from components.trayectoria import entrada_experiencia, entrada_formacion
from servicios.contenido import obtener_perfil, obtener_trayectoria

perfil = obtener_perfil()
trayectoria = obtener_trayectoria()

st.title("Sobre mí", anchor=False)
st.caption(f":material/location_on: {perfil.ubicacion}")
st.markdown(perfil.presentacion)
if perfil.aprendiendo:
    st.caption(f":material/school: Aprendiendo ahora: {perfil.aprendiendo}")

st.header("Experiencia", divider="gray", anchor=False)
for experiencia in trayectoria.experiencia:
    entrada_experiencia(experiencia)

st.header("Formación", divider="gray", anchor=False)
for formacion in trayectoria.formacion:
    entrada_formacion(formacion)

st.header("Idiomas", divider="gray", anchor=False)
st.markdown(insignias(f"{i.idioma} · {i.nivel}" for i in trayectoria.idiomas))
