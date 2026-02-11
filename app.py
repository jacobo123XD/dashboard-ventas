import streamlit as st
import pandas as pd
import plotly.express as px

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Dashboard Excel", layout="wide")
st.title("📊 Mi Dashboard desde Excel")

# --- PASO 1: SUBIR EL ARCHIVO ---
st.sidebar.header("Cargar Datos")
uploaded_file = st.sidebar.file_uploader("Sube tu archivo Excel aquí (.xlsx)", type=["xlsx"])

if uploaded_file is None:
    st.info("👋 **Para empezar:** Por favor sube un archivo Excel en la barra lateral.")
    st.info("Tu Excel debe tener columnas llamadas: **Vendedor**, **Producto**, **Ventas**, **Ciudad**.")
    st.stop() # Detiene la app hasta que subas el archivo

# --- PASO 2: LEER EL ARCHIVO ---
# Si llegamos aquí, es porque el usuario subió un archivo
df = pd.read_excel(uploaded_file)

# --- PASO 3: FILTROS ---
st.sidebar.header("Filtros")

# Filtro: Ciudad
# Verificamos si la columna existe para evitar errores
if "Ciudad" in df.columns:
    ciudad = st.sidebar.multiselect(
        "Filtrar por Ciudad:",
        options=df["Ciudad"].unique(),
        default=df["Ciudad"].unique()
    )
else:
    ciudad = [] # Si no hay columna ciudad, no filtramos nada
    st.warning("⚠️ Tu Excel no tiene una columna 'Ciudad'")

# Filtro: Vendedor
if "Vendedor" in df.columns:
    vendedor = st.sidebar.multiselect(
        "Filtrar por Vendedor:",
        options=df["Vendedor"].unique(),
        default=df["Vendedor"].unique()
    )
    # Aplicar filtros
    if ciudad: # Si hay filtro de ciudad
        df = df.query("Ciudad == @ciudad")
    df_selection = df.query("Vendedor == @vendedor")
else:
    df_selection = df
    st.warning("⚠️ Tu Excel no tiene una columna 'Vendedor'")


# --- PASO 4: KPI's (Indicadores) ---
st.markdown("---")

# Verificamos que exista la columna Ventas para calcular
if "Ventas" in df_selection.columns:
    total_ventas = int(df_selection["Ventas"].sum())
    promedio_venta = round(df_selection["Ventas"].mean(), 2)
    
    col1, col2, col3 = st.columns(3)
    col1.metric("💰 Ventas Totales", f"{total_ventas:,}")
    col2.metric("📈 Promedio", f"{promedio_venta:,}")
    col3.metric("🛒 Registros", df_selection.shape[0])
else:
    st.error("Error: Tu Excel necesita una columna llamada 'Ventas' con números.")
    st.stop()

st.markdown("---")

# --- PASO 5: GRÁFICOS ---
col_graf1, col_graf2 = st.columns(2)

with col_graf1:
    if "Producto" in df_selection.columns:
        st.subheader("Ventas por Producto")
        fig_prod = px.bar(df_selection, x="Producto", y="Ventas", color="Producto", template="plotly_white")
        st.plotly_chart(fig_prod, use_container_width=True)

with col_graf2:
    st.subheader("Ventas por Vendedor")
    fig_vend = px.pie(df_selection, values="Ventas", names="Vendedor", hole=0.5)
    st.plotly_chart(fig_vend, use_container_width=True)

# --- MOSTRAR TABLA ---
with st.expander("Ver Datos del Excel"):
    st.dataframe(df_selection)