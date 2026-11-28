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

## Skill oficial de Streamlit

- Usa la skill `developing-with-streamlit` antes de escribir o cambiar código de Streamlit.
- Instalada en modo global (`~/.claude/skills/`) porque Windows no permite symlinks sin Modo de desarrollador.
- Su script de descubrimiento no detecta el entorno Conda por sí solo: pásale siempre
  `--python "C:/Users/valen/miniconda3/envs/portfolio/python.exe"`.
- Si su documentación difiere de lo que recuerdas de Streamlit, manda la documentación.

## Arquitectura

Separar **contenido**, **presentación** y **lógica**:

```
app.py            # entrada: st.set_page_config + st.navigation (iconos Material + help en cada st.Page)
app_pages/        # vistas (NO `pages/`: choca con el auto-discovery antiguo). Scripts directos, sin funciones envoltorio
servicios/        # puente páginas ↔ core: caché (`st.cache_data`) del contenido; futuro cliente de la API
components/       # UI reutilizable: reciben objetos y los pintan, no leen archivos
core/             # modelos (dataclasses + Enum de estado) y carga de contenido. NO importa streamlit
content/          # datos en TOML (tomllib) + Markdown por proyecto. Todo texto personal vive aquí
assets/           # privado, ignorado por Git (*.pdf)
static/           # PÚBLICO: se sirve en /app/static/ (enableStaticServing). Certificados y documentos
tests/            # pytest: core/ (carga y validación) + páginas con AppTest
.streamlit/config.toml  # tema
```

Convenciones:
- Ningún texto personal escrito a mano dentro de `app_pages/` o `components/`; todo sale de `content/`.
- Lectura de contenido cacheada con `@st.cache_data`.
- Estilo primero con el tema de `config.toml`; CSS personalizado mínimo, solo en `assets/styles.css`.
- Evitar el aspecto de dashboard (navegación superior, sin sidebar si es posible).
- `requirements.txt` con versiones fijadas como fuente de dependencias para el despliegue; `requirements-dev.txt` para pytest y ruff.

## Datos personales

- Fuente de verdad del contenido: el CV, publicado en `static/documentos/cv-valentin-tigovan.pdf`.
- Decisión del usuario: el CV (con su teléfono y email) y la carta de recomendación de DSH se publican.
  Fuera de esos PDFs, **no escribir teléfono ni email** en el contenido de la web.
- Contacto: **formulario** en la página Contacto → email por SMTP (`smtplib`) desde la cuenta del dueño, visitante en Reply-To.
  Credenciales solo en `st.secrets` (`[contacto]`, ver `.streamlit/secrets.toml.example`). Sin secretos, el formulario se oculta.
  Validación en servidor (`core/contacto.py`) además de la del navegador; límite de 3 envíos por sesión y 60 s entre intentos.

## Archivos públicos (`static/`)

- Todo lo que hay en `static/` se publica en la web **y** en el repo público: revisar cada archivo antes
  (DNI, teléfonos, emails, datos de terceros). Nombres en minúsculas, sin espacios ni datos personales.
- En el contenido se referencian como rutas relativas a `static/` (`certificados/x.pdf`); el cargador
  valida que existan y que no salgan de `static/`. `components/enlaces.url_publica()` genera la URL.

## Futura integración ML (no implementar todavía)

- Streamlit será solo **cliente HTTP** de la API; nunca cargará el modelo.
- Llamadas a la API encapsuladas en `servicios/api_credito.py`; URL en `st.secrets`.
- Si la API no responde, mostrar un mensaje claro sin romper el resto de la web.
- En la v1 solo existe el campo opcional `demo_url` en el modelo `Proyecto`.

## Comandos

```
conda activate portfolio
pip install -r requirements-dev.txt  # primera vez: app + pytest + ruff
streamlit run app.py          # ejecutar en local
pytest                        # tests
ruff check . && ruff format . # lint y formato
```

## Proyectos del portfolio

Datos completos en `content/`. Resumen:
1. **Predicción de riesgo de crédito** (destacado): Machine Learning. Estado: TODO.
2. **Automatización de contenido para redes**: IA generativa, prueba de concepto, hecho en las prácticas de Data Science Hub.
3. **BuyPilot**: TFG de DAW en equipo de 3; el usuario hizo el backend. Estado: TODO.

## Decisiones pendientes

Estado de los proyectos 1 y 3 ·
capturas · idioma (solo ES o ES+EN) · foto ·
dataset y licencia del proyecto de crédito · repo de la API (mismo o aparte) · hibernación de Community Cloud.

Resueltas: repos de proyectos, LinkedIn y certificados enlazados (sacados del CV) · repositorio público https://github.com/ValentinIA/portfolio · app publicada en https://valentin-portfolio.streamlit.app/ · Streamlit 1.67.0 admite `st.navigation(position="top")`.

## Fase actual

Fase 5: diseño, en revisión visual con el usuario. Fases 0–4 completadas.
Diseño decidido: tema **oscuro fijo** (azul + slate, Inter) en `.streamlit/config.toml`; `layout="wide"` con
columnas (principal a la izquierda, secundario a la derecha); sin divisores; contraste WCAG AA (≥ 4.5:1).
Hoja de ruta: 0 base → 1 despliegue temprano → 2 esqueleto de navegación → 3 modelo de contenido → 4 páginas → 5 diseño → 6 revisión y cierre.
