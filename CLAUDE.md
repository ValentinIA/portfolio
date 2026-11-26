# CLAUDE.md — Portfolio profesional (Python + Streamlit)

## Qué es este proyecto

Portfolio personal para buscar empleo como desarrollador **Python junior** (backend, Data Science, ML aplicado).
Público: reclutadores técnicos y equipos de backend / Data Science.
Objetivo secundario: aprender desarrollo agéntico con Claude Code.

## Cómo trabajar conmigo (prioritario)

- Actúa como **arquitecto senior y mentor**: explica cada decisión técnica y cada concepto nuevo.
- Trabaja en **fases pequeñas**. No generes el proyecto entero de golpe.
- Antes de cada fase, resume qué vas a hacer y espera mi aprobación si cambia la arquitectura.
- No instales dependencias sin decirme antes cuáles y por qué.
- Responde en **español**. Código, nombres de variables y commits en español.

## Reglas de contenido (no negociables)

- **No inventes** resultados, métricas, funcionalidades ni datos sobre mis proyectos o mi experiencia.
- Cada proyecto debe declarar su estado: `funcional`, `prototipo` o `prueba de concepto`.
- Si falta un dato, déjalo como `TODO` visible y pregúntame. Nunca lo rellenes con algo plausible.
- El desarrollo agéntico se menciona como aprendizaje, **no** como especialidad.

## Stack

- Python 3.11, entorno Conda `portfolio` (`conda activate portfolio`).
- Streamlit (única dependencia de ejecución en la v1).
- Git + GitHub. Despliegue en Streamlit Community Cloud.
- Sin frameworks frontend (React, Next.js…) salvo razón técnica justificada.
- Futuro: API independiente con FastAPI para el modelo de riesgo de crédito.

## Arquitectura

Separar **contenido**, **presentación** y **lógica**:

```
app.py            # entrada: st.set_page_config + st.navigation (no carpeta pages/ automática)
pages/            # vistas: inicio, proyectos (listado + detalle vía ?p=slug), sobre_mi, contacto
components/       # UI reutilizable: reciben objetos y los pintan, no leen archivos
core/             # modelos (dataclasses + Enum de estado) y carga de contenido. NO importa streamlit
content/          # datos en TOML (tomllib) + Markdown por proyecto. Todo texto personal vive aquí
assets/           # cv.pdf, styles.css, images/
tests/            # pytest sobre core/
.streamlit/config.toml  # tema
```

Convenciones:
- Ningún texto personal escrito a mano dentro de `pages/` o `components/`; todo sale de `content/`.
- Lectura de contenido cacheada con `@st.cache_data`.
- Estilo primero con el tema de `config.toml`; CSS personalizado mínimo, solo en `assets/styles.css`.
- Evitar el aspecto de dashboard (navegación superior, sin sidebar si es posible).
- `requirements.txt` con versiones fijadas como fuente de dependencias para el despliegue; `requirements-dev.txt` para pytest y ruff.

## Futura integración ML (no implementar todavía)

- Streamlit será solo **cliente HTTP** de la API; nunca cargará el modelo.
- Llamadas a la API encapsuladas en `services/credit_api.py`; URL en `st.secrets`.
- Si la API no responde, mostrar un mensaje claro sin romper el resto de la web.
- En la v1 solo existe el campo opcional `demo_url` en el modelo `Project`.

## Comandos

```
conda activate portfolio
streamlit run app.py          # ejecutar en local
pytest                        # tests
ruff check . && ruff format . # lint y formato
```

## Proyectos del portfolio

1. **Predicción de riesgo de crédito** (destacado): clasificación supervisada; Pandas, Scikit-learn, Matplotlib, Joblib. Estado: TODO.
2. **BuyPilot**: comparador de precios; FastAPI, MySQL, Crawl4AI, Docker, Uvicorn. Estado: TODO.
3. **Automatización de contenido para redes**: prueba de concepto; Streamlit, OpenAI API, Whisper, SQLite.

## Decisiones pendientes

Estado de los proyectos 1 y 2 · repos públicos enlazables · capturas · email/LinkedIn/GitHub ·
CV en PDF · idioma (solo ES o ES+EN) · foto · dataset y licencia del proyecto de crédito ·
repo de la API (mismo o aparte) · hibernación de Community Cloud.

Resueltas: repositorio público https://github.com/ValentinIA/portfolio · app publicada en https://valentin-portfolio.streamlit.app/ · Streamlit 1.67.0 admite `st.navigation(position="top")`.

## Fase actual

Fase 2: esqueleto de navegación (4 páginas vacías con `st.navigation` superior). Fases 0 y 1 completadas.
Hoja de ruta: 0 base → 1 despliegue temprano → 2 esqueleto de navegación → 3 modelo de contenido → 4 páginas → 5 diseño → 6 revisión y cierre.
