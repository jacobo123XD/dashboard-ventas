import streamlit as st
import pandas as pd
import plotly.express as px

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Dashboard Ventas", layout="wide")

# --- TÍTULO PRINCIPAL ---
st.title("📊 Reporte de Ventas Interactivo")
st.markdown("---")

# --- 1. SIMULACIÓN DE DATOS (Como si leyeras un Excel) ---
# En la vida real, aquí usarías: df = pd.read_excel("tu_archivo.xlsx")
data = {
    'Fecha': ['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04', '2023-01-05'] * 4,
    'Vendedor': ['Carlos', 'Maria', 'Carlos', 'Ana', 'Maria'] * 4,
    'Producto': ['Laptop', 'Mouse', 'Teclado', 'Monitor', 'Laptop'] * 4,
    'Ventas': [1200, 45, 80, 300, 1150, 1300, 50, 90, 310, 1200, 1250, 60, 85, 320, 1100, 1180, 40, 75, 290, 1120],
    'Ciudad': ['Santo Domingo', 'Santiago', 'Santo Domingo', 'Punta Cana', 'Santiago'] * 4
}
df = pd.DataFrame(data)

# --- 2. BARRA LATERAL (FILTROS) ---
st.sidebar.header("Filtros")

# Filtro por Ciudad
ciudad = st.sidebar.multiselect(
    "Selecciona Ciudad:",
    options=df["Ciudad"].unique(),
    default=df["Ciudad"].unique()
)

# Filtro por Vendedor
vendedor = st.sidebar.multiselect(
    "Selecciona Vendedor:",
    options=df["Vendedor"].unique(),
    default=df["Vendedor"].unique()
)

# Aplicar filtros a la tabla de datos
df_selection = df.query(
    "Ciudad == @ciudad & Vendedor == @vendedor"
)

# --- 3. KPIs (INDICADORES PRINCIPALES) ---
total_ventas = int(df_selection["Ventas"].sum())
promedio_venta = round(df_selection["Ventas"].mean(), 2)
cantidad_transacciones = df_selection.shape[0]

col1, col2, col3 = st.columns(3)
col1.metric("💰 Ventas Totales", f"RD$ {total_ventas:,}")
col2.metric("📈 Venta Promedio", f"RD$ {promedio_venta:,}")
col3.metric("🛒 Transacciones", cantidad_transacciones)

st.markdown("---")

# --- 4. GRÁFICOS INTERACTIVOS ---

col_grafico1, col_grafico2 = st.columns(2)

# Gráfico de Barras (Ventas por Producto)
with col_grafico1:
    st.subheader("Ventas por Producto")
    fig_product = px.bar(
        df_selection,
        x="Producto",
        y="Ventas",
        color="Producto",
        template="plotly_white"
    )
    st.plotly_chart(fig_product, use_container_width=True)

# Gráfico Circular (Ventas por Vendedor)
with col_grafico2:
    st.subheader("Participación por Vendedor")
    fig_vendedor = px.pie(
        df_selection,
        values="Ventas",
        names="Vendedor",
        hole=0.5
    )
    st.plotly_chart(fig_vendedor, use_container_width=True)


# --- 5. MOSTRAR DATOS CRUDOS ---
# Checkbox para ocultar/mostrar la tabla
if st.checkbox("Ver Tabla de Datos Detallada"):
    st.dataframe(df_selection)

# --- FIN DEL CÓDIGO ---