import streamlit as st
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import folium
from streamlit_folium import folium_static
from folium.plugins import FastMarkerCluster
import altair as alt


# Configuración inicial
sns.set()
alt.data_transformers.disable_max_rows()

# Cargar datos
listings = pd.read_csv('df_finals/listings.csv')
listings_details = pd.read_csv('df_finals/listings_details.csv')
neighbourhoods = pd.read_csv('df_finals/neighbourhoods.csv')
delitos = pd.read_csv('df_finals/delitos.csv')
delitos_sorted_transposed = pd.read_csv('df_finals/delitos_sorted_transposed.csv')

def main():
    # Configurar la página
    st.set_page_config(page_title="AirBnb en Buenos Aires", layout="wide")

    # Sidebar
    st.sidebar.title("Análisis de AirBnB en Buenos Aires")
    selected_page = st.sidebar.radio("Selecciona una sección", ["Inicio", "Conociendo Buenos Aires", "Seguridad en Buenos Aires", "Buscador Interactivo"])

    # Contenido principal basado en la selección del sidebar
    if selected_page == "Inicio":
        mostrar_inicio()
    elif selected_page == "Conociendo Buenos Aires":
        mostrar_seccion1()
    elif selected_page == "Seguridad en Buenos Aires":
        mostrar_seccion2()
    elif selected_page == "Buscador Interactivo":
        mostrar_seccion3()

def mostrar_inicio():
    st.title("Bienvenidos a la Ciudad de la Furia")
    st.write("A continuación, presentación con resumen ejecutivo del análisis")
    st.markdown('<iframe src="https://prezi.com/p/embed/P3UKvZFbMkFh4h0Hs17M/" '
                'id="iframe_container" frameborder="0" webkitallowfullscreen="" '
                'mozallowfullscreen="" allowfullscreen="" '
                'allow="autoplay; fullscreen" height="315" width="560"></iframe>',
                unsafe_allow_html=True)

def mostrar_seccion1():
    st.title("Conociendo Buenos Aires desde la óptica de AirBnB")
    st.write("Realizamos un Análisis Exploratorio de Datos")

    # Número de unidades de BnB's por Barrio
    mostrar_treemap(listings["neighbourhood"].value_counts(), "Número de unidades", "Barrio", "Barrios y unidades de BnB's")

    # Mapa de unidades de BnB's disponibles
    mostrar_mapa(listings['latitude'], listings['longitude'], "Mapa de unidades de BnB's disponibles")

    # Análisis de Tipo de Habitación en AirBnB
    mostrar_treemap(listings['room_type'].value_counts(), "Número de unidades", "Tipo de habitación", "Tipo de habitación del alojamiento")

    # Análisis de Unidades según Acomodaciones en AirBnB
    mostrar_treemap(listings_details['accommodates'].value_counts().sort_index(), "Cantidad de unidades", "Huéspedes", "Unidades según acomodaciones (número de huéspedes)")

def mostrar_seccion2():
    st.title("Seguridad en Buenos Aires")
    st.write("Realizamos un Análisis Estadístico para evaluarlo")

    # Planteo de Hipótesis
    st.markdown("## Planteo de Hipótesis:")
    st.markdown("### A pesar de que medios como [El Español](https://www.elespanol.com/malaga/vivir/20230515/buenos-aires-ciudad-segura-viajar/763923781_0.html) o [Lonely Planet](https://www.lonelyplanet.es/america-del-sur/argentina/buenos-aires/seguridad-y-alertas) hacen recomendaciones sobre barrios seguros en Buenos Aires, hemos realizado un análisis estadístico y se concluye que *no hay diferencia* significativa en la seguridad *entre los barrios de Buenos Aires* considerados como seguros y aquellos que no se consideran seguros. En otras palabras, la tasa de incidentes delictivos reales en los barrios mencionados como seguros es igual a la tasa en los barrios no mencionados.")

    # Filtrar por variable y valor
    mostrar_datos_filtrados(delitos, "Barrio", st.sidebar.selectbox("Seleccionar Variable", delitos.columns))

def mostrar_seccion3():
    st.title("Buscador Interactivo")
    st.write("Puede aplicar filtros para buscar sobre los datos de los AirBnB en Buenos Aires")

    # Filtrar por variable y valor
    mostrar_datos_filtrados(listings, "neighbourhood", st.sidebar.selectbox("Seleccionar Variable", listings.columns))

    # Filtrar por rango de precios
    mostrar_filtros_rango_precios(listings)

    # Filtrar por rango de accommodates
    mostrar_grafico_accommodates(listings_details)

def mostrar_treemap(data, values_column, path_column, title):
    color_scale = px.colors.sequential.Pinkyl
    fig = px.treemap(data, path=[path_column], values=values_column, color=values_column,
                     color_continuous_scale=color_scale,
                     labels={values_column: f"Número de {values_column}", path_column: path_column})

    fig.update_traces(textinfo="label+percent entry", hoverinfo="label+value+percent parent",
                      hovertemplate=f'<b>%{{label}}</b><br>%{{value}} {values_column}<br>%{{percentParent:.2%}} del total')

    fig.update_layout(
        font=dict(family="Montserrat, sans-serif"),
        title_font=dict(family="Montserrat, sans-serif", size=20),
        legend_font=dict(family="Montserrat, sans-serif")
    )

    # Mostrar el gráfico en la aplicación de Streamlit
    st.plotly_chart(fig)

def mostrar_mapa(latitude, longitude, title):
    locations = list(zip(latitude, longitude))
    map1 = folium.Map(location=[-34.603728759790506, -58.381548802904966], zoom_start=10.5)
    FastMarkerCluster(data=locations).add_to(map1)
    # Mostrar el mapa de Folium en Streamlit
    folium_static(map1)

def mostrar_datos_filtrados(data, default_column, selected_column):
    st.markdown(f"## Explorador de Datos de {data.name}")
    # Barra lateral para selección de variable y valor
    variable_seleccionada = st.sidebar.selectbox("Seleccionar Variable", data.columns, key="variable_selector")
    valores_unicos = data[variable_seleccionada].unique()
    filtro_valor = st.sidebar.selectbox(f"Filtrar por Valor de {variable_seleccionada}", ["Todos"] + list(valores_unicos))

    # Filtrar el DataFrame según la variable y el valor seleccionados
    if filtro_valor != "Todos":
        datos_filtrados = data[data[variable_seleccionada] == filtro_valor]
    else:
        datos_filtrados = data

    # Mostrar el DataFrame filtrado en la interfaz de usuario
    st.sidebar.write(f"Filtrar por {variable_seleccionada}:", filtro_valor)
    st.write(datos_filtrados)

    # Mostrar gráfico según el tipo de variable
    if data[variable_seleccionada].dtype == 'O':  # Variable categórica
        plt.figure(figsize=(12, 6))
        sns.countplot(x=variable_seleccionada, data=datos_filtrados, color='red')
        plt.title(f'{variable_seleccionada} por Barrio')
        plt.xlabel(variable_seleccionada)
        plt.ylabel('Cantidad')
        plt.xticks(rotation=90)  # Rotar las etiquetas del eje x a 90 grados
        st.pyplot(plt)
    elif data[variable_seleccionada].dtype in ['float64', 'int64']:  # Variable numérica
        st.write(f"**Estadísticas de {variable_seleccionada}:**")
        st.write(datos_filtrados[variable_seleccionada].describe())

def mostrar_filtros_rango_precios(data):
    st.markdown("## Explorador de Precios y Barrios de Listados de Airbnb")
    # Barra lateral para selección de rango de precios
    precio_minimo, precio_maximo = st.sidebar.slider("Seleccionar Rango de Precios", float(data['price'].min()), float(data['price'].max()), (float(data['price'].min()), float(data['price'].max())))

    # Filtrar el DataFrame según el rango de precios seleccionado
    datos_filtrados = data[(data['price'] >= precio_minimo) & (data['price'] <= precio_maximo)]

    # Contar la cantidad de registros por barrio en el rango de precios seleccionado
    conteo_por_barrio = datos_filtrados['neighbourhood'].value_counts()

    # Mostrar los datos en la aplicación
    st.sidebar.write(f"Filtrar por Rango de Precios: {precio_minimo} a {precio_maximo}")
    st.write(conteo_por_barrio)

    # También puedes mostrar un gráfico de barras para visualizar la información
    st.bar_chart(conteo_por_barrio)

def mostrar_grafico_accommodates(data):
    st.markdown("## Explorador de Accommodates y Neighborhoods de Listados de Airbnb")
    # Barra lateral para selección de rango de accommodates
    accommodates_min, accommodates_max = st.sidebar.slider("Seleccionar Rango de Accommodates", int(data['accommodates'].min()), int(data['accommodates'].max()), (int(data['accommodates'].min()), int(data['accommodates'].max())))

    # Filtrar el DataFrame según el rango de accommodates seleccionado
    datos_filtrados = data[(data['accommodates'] >= accommodates_min) & (data['accommodates'] <= accommodates_max)]

    # Gráfico de barras agrupado por neighborhoods
    bar_chart = alt.Chart(datos_filtrados).mark_bar().encode(
        x='neighbourhood_cleansed:N',
        y='count():Q',
        color='neighbourhood_cleansed:N'
    ).properties(
        width=800,
        height=400,
        title=f'Distribución de Accommodates por Neighborhoods (Rango: {accommodates_min} a {accommodates_max})'
    )

    # Mostrar el gráfico en la aplicación
    st.sidebar.write(f"Filtrar por Rango de Accommodates: {accommodates_min} a {accommodates_max}")
    st.altair_chart(bar_chart, use_container_width=True)

if __name__ == "__main__":
    main()
