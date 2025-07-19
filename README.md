
# Dashboard Planificación Cambio Climático 🇪🇨

Este repositorio contiene una aplicación **Streamlit** para visualizar de forma interactiva
la matriz de planificación de proyectos relacionados con cambio climático en Ecuador.

## Estructura

```
.
├── app.py                        # Aplicación principal de Streamlit
├── requirements.txt              # Dependencias
├── 00_Planificacion_CambioClimatico_dashboard_2025jul19_2.xlsx  # Datos de origen
```

## Cómo ejecutar localmente

1. Clona este repositorio o descarga los archivos.
2. Crea un entorno virtual (recomendado) e instala las dependencias:

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

3. Inicia la aplicación:

```bash
streamlit run app.py
```

La aplicación se abrirá en tu navegador predeterminado (`http://localhost:8501`).

## Publicar en Streamlit Community Cloud

1. Sube este repositorio a **GitHub**.
2. Ve a [streamlit.io](https://streamlit.io/) e inicia sesión.
3. Haz clic en **'New app'**, selecciona tu repositorio, la rama principal y el archivo `app.py`.
4. ¡Listo! En pocos minutos tendrás tu dashboard en línea de forma gratuita.

## Notas

- El mapa requiere conexión a internet para descargar el `GeoJSON` de las provincias del Ecuador.
- Si deseas estilo personalizado puedes modificar los colores o agregar componentes adicionales en `app.py`.
