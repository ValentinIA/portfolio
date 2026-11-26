"""Entradas de experiencia y formación para la página Sobre mí."""

import streamlit as st

from core.modelos import Experiencia, Formacion


def _entrada(
    titulo: str,
    organizacion: str,
    periodo: str,
    descripcion: str | None,
    credencial_url: str | None,
) -> None:
    with st.container(border=True):
        with st.container(
            horizontal=True, horizontal_alignment="distribute", vertical_alignment="center"
        ):
            st.markdown(f"**{titulo}**")
            st.caption(periodo)
        st.caption(organizacion)
        if descripcion:
            st.markdown(descripcion)
        if credencial_url:
            st.page_link(credencial_url, label="Ver certificado", icon=":material/verified:")


def entrada_experiencia(experiencia: Experiencia) -> None:
    _entrada(
        experiencia.puesto,
        experiencia.empresa,
        experiencia.periodo,
        experiencia.descripcion,
        experiencia.credencial_url,
    )


def entrada_formacion(formacion: Formacion) -> None:
    _entrada(
        formacion.titulo,
        formacion.centro,
        formacion.periodo,
        formacion.descripcion,
        formacion.credencial_url,
    )
