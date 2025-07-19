
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import folium
from streamlit_folium import folium_static

st.set_page_config(layout="wide", page_title="Dashboard Cambio Climático")

@st.cache_data
def load_data():
    return pd.read_excel("00_Planificacion_CambioClimatico_dashboard_2025jul19_2.xlsx")

df = load_data()

projects = df["Siglas proyecto"].dropna().unique().tolist()
selected_project = st.sidebar.selectbox("Filtrar por proyecto", ["Todos"] + projects)

if selected_project != "Todos":
    dff = df[df["Siglas proyecto"] == selected_project]
else:
    dff = df.copy()

st.title("Dirección de Riesgos y Aseguramiento Agropecuario - Cambio Climático")

tab1, tab2 = st.tabs(["Visión General", "Mapa"])

with tab1:
    col1, col2 = st.columns([2,1])
    with col1:
        st.subheader("Beneficiarios por proyecto")
        pie = px.pie(dff, names="Siglas proyecto", values="Beneficiarios (personas productoras)", hole=0.5,
                     height=400)
        st.plotly_chart(pie, use_container_width=True)
    with col2:
        st.subheader("Avance global promedio")
        if not dff["Porcentaje de avance global"].dropna().empty:
            avg_progress = dff["Porcentaje de avance global"].mean()
        else:
            avg_progress = 0
        gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=avg_progress,
            number={'suffix': "%"},
            gauge={'axis': {'range': [None, 100]},
                   'bar': {'color': "royalblue"},
                   'steps':[
                       {'range':[0,50],'color':'lightgray'},
                       {'range':[50,100],'color':'gray'}]},
        ))
        gauge.update_layout(height=400, margin=dict(l=40,r=40))
        st.plotly_chart(gauge, use_container_width=True)

    st.markdown("---")
    col3, col4 = st.columns(2)
    with col3:
        st.subheader("Distribución de financiamiento")
        if not dff.empty:
            bar = px.bar(dff, x="Financiamiento (entidad)", y="Superficie intervenida (ha)", color="Siglas proyecto",
                         orientation="v", height=350)
            st.plotly_chart(bar, use_container_width=True)
        else:
            st.info("No hay datos para mostrar este gráfico.")
    with col4:
        st.subheader("Cantidad de proyectos por fase")
        if not dff.empty:
            stage_counts = dff["Fase"].value_counts().reset_index()
            stage_counts.columns=["Fase","Proyectos"]
            area = px.area(stage_counts, x="Fase", y="Proyectos", height=350)
            st.plotly_chart(area, use_container_width=True)
        else:
            st.info("No hay datos para mostrar este gráfico.")

with tab2:
    st.subheader("Ubicacion")
    map_df = dff.groupby("Ubicación", as_index=False).agg({"Superficie intervenida (ha)":"sum"})
    if map_df.empty or map_df["Ubicación"].isna().all():
        st.info("Sin datos de ubicación para mostrar el mapa.")
    else:
        import requests
        url = "https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/ecuador-provinces.geojson"
        try:
            geojson = requests.get(url).json()
            m = folium.Map(location=[-1.25,-78.58], zoom_start=6, tiles="cartodbpositron")
            chor = folium.Choropleth(
                geo_data=geojson,
                data=map_df,
                columns=["Ubicación","Superficie intervenida (ha)"],
                key_on="feature.properties.name",
                fill_color="YlGn",
                fill_opacity=0.7,
                line_opacity=0.2,
                legend_name="Superficie (ha)"
            ).add_to(m)
            folium.LayerControl().add_to(m)
            folium_static(m, width=1100, height=600)
        except Exception as e:
            st.error(f"No se pudo cargar el mapa: {e}")
