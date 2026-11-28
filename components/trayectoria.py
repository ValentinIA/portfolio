"""Entradas de experiencia y formación para la página Sobre mí."""

import streamlit as st

from components.enlaces import enlace_recurso
from core.modelos import Experiencia, Formacion


def _entrada(
    titulo: str,
    organizacion: str,
    periodo: str,
    descripcion: str | None,
    certificados: tuple[str, ...],
    carta_recomendacion: str | None = None,
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
        if certificados:
            # En fila, uno al lado del otro (se reparten en varias líneas si no caben).
            with st.container(horizontal=True, gap="small"):
                for numero, certificado in enumerate(certificados, start=1):
                    # Con varios certificados se numeran: "Ver certificado 1", "Ver certificado 2".
                    etiqueta = "Ver certificado" + (f" {numero}" if len(certificados) > 1 else "")
                    enlace_recurso(etiqueta, certificado, ":material/verified:")
        if carta_recomendacion:
            enlace_recurso(
                "Ver carta de recomendación", carta_recomendacion, ":material/recommend:"
            )


def entrada_experiencia(experiencia: Experiencia) -> None:
    _entrada(
        experiencia.puesto,
        experiencia.empresa,
        experiencia.periodo,
        experiencia.descripcion,
        experiencia.certificados,
        experiencia.carta_recomendacion,
    )


def entrada_formacion(formacion: Formacion) -> None:
    _entrada(
        formacion.titulo,
        formacion.centro,
        formacion.periodo,
        formacion.descripcion,
        formacion.certificados,
    )
