import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard South Park", layout="wide")
st.title("Explorador de Personajes - South Park")

# 1. Carga segura de datos (Evita el EmptyDataError)
@st.cache_data
def cargar_datos_seguro():
    try:
        df_pers = pd.read_csv('datos/personajes.csv')
        df_det = pd.read_csv('datos/detalles_personajes.csv')
        
        # Comprobar si están vacíos
        if df_pers.empty or df_det.empty:
            return None
            
        return pd.merge(df_pers, df_det, on='id_personaje')
    except (FileNotFoundError, pd.errors.EmptyDataError):
        return None

df = cargar_datos_seguro()

# Si hay error, mostrar aviso bonito en lugar de error rojo
if df is None:
    st.error("Los archivos CSV no existen o están vacíos.")
    st.info("Solución: Ve a tu terminal, detén Streamlit (presiona Ctrl+C) y ejecuta primero: `python scraper.py`")
    st.stop()

# 2. Interfaz y Filtros
st.sidebar.header("Filtros")
categorias = sorted(df['categoria'].unique())
seleccion = st.sidebar.multiselect("Filtrar Categoría:", options=categorias, default=categorias)

df_filtrado = df[df['categoria'].isin(seleccion)]

# 3. Métricas y Tabla
col1, col2 = st.columns(2)
col1.metric("Personajes Mostrados", len(df_filtrado))
col2.metric("Categorías", len(seleccion))

st.subheader("Datos Extraídos")
st.dataframe(df_filtrado[['id_personaje', 'nombre', 'categoria', 'descripcion']], use_container_width=True)

# 4. Gráfico
st.subheader("Distribución")
if not df_filtrado.empty:
    grafico = px.bar(
        df_filtrado.groupby('categoria').size().reset_index(name='Cantidad'),
        x='categoria', y='Cantidad', color='categoria',
        title="Personajes por Categoría"
    )
    st.plotly_chart(grafico, use_container_width=True)