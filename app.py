"""Punto de entrada del portfolio.

Streamlit ejecuta este archivo en cada interacción. Aquí solo se configura
la página y se define la navegación; el contenido de cada sección vive
en su propio archivo dentro de pages/.
"""

import streamlit as st

st.set_page_config(page_title="Portfolio", layout="centered")

paginas = [
    st.Page("pages/inicio.py", title="Inicio", default=True),
    st.Page("pages/proyectos.py", title="Proyectos", url_path="proyectos"),
    st.Page("pages/sobre_mi.py", title="Sobre mí", url_path="sobre-mi"),
    st.Page("pages/contacto.py", title="Contacto", url_path="contacto"),
]

pagina_actual = st.navigation(paginas, position="top")
pagina_actual.run()
