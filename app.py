"""Punto de entrada del portfolio.

Streamlit ejecuta este archivo en cada interacción. Aquí solo se configura
la página y se define la navegación; el contenido de cada sección vive
en su propio archivo dentro de app_pages/.
"""

import streamlit as st

st.set_page_config(page_title="Portfolio", page_icon=":material/code:", layout="wide")

paginas = [
    st.Page(
        "app_pages/inicio.py",
        title="Inicio",
        icon=":material/home:",
        default=True,
        help="Presentación profesional, tecnologías principales y proyecto destacado.",
    ),
    st.Page(
        "app_pages/proyectos.py",
        title="Proyectos",
        icon=":material/folder_open:",
        url_path="proyectos",
        help="Catálogo de proyectos con su estado, tecnologías y detalle de cada uno.",
    ),
    st.Page(
        "app_pages/sobre_mi.py",
        title="Sobre mí",
        icon=":material/person:",
        url_path="sobre-mi",
        help="Perfil, experiencia, formación e idiomas.",
    ),
    st.Page(
        "app_pages/contacto.py",
        title="Contacto",
        icon=":material/mail:",
        url_path="contacto",
        help="Enlaces profesionales y vías de contacto.",
    ),
]

pagina_actual = st.navigation(paginas, position="top")
pagina_actual.run()
