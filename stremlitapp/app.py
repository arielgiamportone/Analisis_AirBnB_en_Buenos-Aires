import streamlit as st
import numpy as np
import pandas as pd
import seaborn as sns
sns.set()
import matplotlib.pyplot as plt
import os
import json
import folium
from streamlit_folium import folium_static
from folium.plugins import FastMarkerCluster
import geopandas as gpd
from branca.colormap import LinearColormap
import altair as alt
import plotly_express as px
from plotly.subplots import make_subplots
import matplotlib.font_manager as fm
import plotly.graph_objs as go
import chart_studio.plotly as py
from plotly.offline import iplot, init_notebook_mode
import cufflinks
cufflinks.go_offline(connected=True)
init_notebook_mode(connected=True)

listings = pd.read_csv("df_finals/listings.csv")
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
    st.write("A continuación presentación con resumen ejecutivo del análisis")
    st.markdown('<iframe src="https://prezi.com/p/embed/P3UKvZFbMkFh4h0Hs17M/" '
                'id="iframe_container" frameborder="0" webkitallowfullscreen="" '
                'mozallowfullscreen="" allowfullscreen="" '
                'allow="autoplay; fullscreen" height="315" width="560"></iframe>',
                unsafe_allow_html=True)

def mostrar_seccion1():
    st.title("Conociendo Buenos Aires desde la óptica de AirBnB")
    st.write("Realizamos un Análisis Exploratorio de Datos")

    st.markdown("## Número de unidades de BnB's por Barrio")

    feq = listings["neighbourhood"].value_counts().sort_values(ascending=True)
    data = pd.DataFrame({"Neighbourhood": feq.index, "Units": feq.values})
    color_scale = px.colors.sequential.Pinkyl
    fig = px.treemap(data, path=["Neighbourhood"], values="Units", color="Units",
                     color_continuous_scale=color_scale,
                     labels={"Units": "Número de unidades", "Neighbourhood": "Barrio"})

    fig.update_traces(textinfo="label+percent entry", hoverinfo="label+value+percent parent",
                      hovertemplate='<b>%{label}</b><br>%{value} unidades<br>%{percentParent:.2%} del total')

    fig.update_layout(
        font=dict(family="Montserrat, sans-serif"),
        title_font=dict(family="Montserrat, sans-serif", size=20),
        legend_font=dict(family="Montserrat, sans-serif")
      
    )
    st.plotly_chart(fig)


    st.markdown("## Mapa de unidades de BnB`s disponibles")
    # Crear un mapa de Folium
    lats = listings['latitude'].tolist()
    lons = listings['longitude'].tolist()
    locations = list(zip(lats, lons))

    map1 = folium.Map(location=[-34.603728759790506, -58.381548802904966], zoom_start=10.5)
    FastMarkerCluster(data=locations).add_to(map1)

    # Mostrar el mapa de Folium en Streamlit
    folium_static(map1)

    st.markdown("## Análisis de Tipo de Habitación en AirBnB")

    # Cargar tus datos (asegúrate de tener 'listings' definido)
    # listings = ...

    # Crear el gráfico de treemap con Plotly Express
    freq = listings['room_type'].value_counts().sort_values(ascending=True)
    data = pd.DataFrame({'Room Type': freq.index, 'Count': freq.values})

    fig = px.treemap(data, path=['Room Type'], values='Count',
                     color='Count', color_continuous_scale='Pinkyl',
                     title="Tipo de habitación del alojamiento",
                     labels={'Count': 'Número de unidades', 'Room Type': 'Tipo de habitación'})

    fig.update_layout(
        font=dict(family="Arial, sans-serif"),
        title_font=dict(family="Arial, sans-serif", size=20),
        legend_title_font=dict(family="Arial, sans-serif"),
        legend_font=dict(family="Arial, sans-serif"),
        margin=dict(l=0, r=0, b=0, t=50)
    )

    # Mostrar el gráfico en la aplicación de Streamlit
    st.plotly_chart(fig)

    st.markdown("## Análisis de Unidades según Acomodaciones en AirBnB")

    # Cargar tus datos (asegúrate de tener 'listings' definido)
    # listings = ...

    # Crear el gráfico de treemap con Plotly Express
    feq = listings_details['accommodates'].value_counts().sort_index()
    data = pd.DataFrame({'Accommodates': feq.index, 'Count': feq.values})

    fig = px.treemap(data, path=['Accommodates'], values='Count', color='Count', color_continuous_scale='Pinkyl',
                     title="Unidades según acomodaciones (número de huéspedes)",
                     labels={'Count': 'Cantidad de unidades', 'Accommodates': 'Huéspedes'})

    fig.update_layout(
        font=dict(family="Arial, sans-serif"),
        title_font=dict(family="Arial, sans-serif", size=25),
        legend_title_font=dict(family="Arial, sans-serif"),
        legend_font=dict(family="Arial, sans-serif"),
    )

    # Mostrar el gráfico en la aplicación de Streamlit
    st.plotly_chart(fig)


    # Ruta del archivo HTML del mapa
    ruta_archivo_html = "Precios_por_barrios.html"

    def mostrar_html():
    # Ruta del archivo HTML
        ruta_archivo_html = 'Precios_por_barrios.html'

    # Mostrar el HTML en la aplicación de Streamlit
    st.markdown("## Mapa de precios promedio de BnB`s por barrios")
    with open(ruta_archivo_html, 'r', encoding='utf-8') as f:
        html_content = f.read()
        st.components.v1.html(html_content, height=800, scrolling=True)

    

def mostrar_seccion2():
    st.title("Seguridad en Buenos Aires")
    st.write("Realizamos un Análisis Estadístico para evaluarlo")

    st.markdown("## Planteo de Hipótesis:")
    st.markdown("### A pesar de que medios como [El Español](https://www.elespanol.com/malaga/vivir/20230515/buenos-aires-ciudad-segura-viajar/763923781_0.html) o [Lonely Planet](https://www.lonelyplanet.es/america-del-sur/argentina/buenos-aires/seguridad-y-alertas) hacen recomendaciones sobre barrios seguros en Buenos Aires, hemos realizado un análisis estadístico y se concluye que *no hay diferencia* significativa en la seguridad *entre los barrios de Buenos Aires* considerados como seguros y aquellos que no se consideran seguros. En otras palabras, la tasa de incidentes delictivos reales en los barrios mencionados como seguros es igual a la tasa en los barrios no mencionados.")
    

    # Barra lateral para selección de variables
    variable_seleccionada = st.sidebar.selectbox("Seleccionar Variable", delitos.columns)

    # Obtener valores únicos de la columna seleccionada
    valores_unicos = delitos[variable_seleccionada].unique()

    # Desplegable para filtrar por valor
    filtro_valor = st.sidebar.selectbox("Filtrar por Valor", ["Todos"] + list(valores_unicos))

    # Filtrar el DataFrame según la variable y el valor seleccionados
    if filtro_valor != "Todos":
        datos_filtrados = delitos[delitos[variable_seleccionada] == filtro_valor]
    else:
        datos_filtrados = delitos

    # Mostrar el DataFrame filtrado en la interfaz de usuario
    st.title("Explorador de Datos de Delitos por Barrio")
    st.sidebar.write("Filtrar por", variable_seleccionada)
    st.write(datos_filtrados)

    # Graficar por barrio
    plt.figure(figsize=(12, 6))
    sns.barplot(x='Barrio', y=variable_seleccionada, data=datos_filtrados, color='red')
    plt.title(f'{variable_seleccionada} por Barrio')
    plt.xlabel('Barrio')
    plt.ylabel(variable_seleccionada)
    plt.xticks(rotation=90)  # Rotar las etiquetas del eje x a 90 grados
    st.pyplot(plt)
    
def mostrar_seccion3():
    st.title("Buscador Interactivo")
    st.write("Puede aplicar filtros para buscar sobre los datos de los AirBnB en Buenos Aires")
    # Barra lateral para selección de variables
    variable_seleccionada = st.sidebar.selectbox("Seleccionar Variable", listings.columns)

    # Obtener valores únicos para el filtro desplegable
    valores_unicos = listings[variable_seleccionada].unique()

    # Barra lateral para filtrar por valor específico (desplegable)
    filtro_valor = st.sidebar.selectbox(f"Seleccionar {variable_seleccionada}", valores_unicos)

    # Intentar filtrar el DataFrame según la variable y el valor seleccionados
    try:
        if filtro_valor:
            # Filtrar por valor si se proporciona
            datos_filtrados = listings[listings[variable_seleccionada] == filtro_valor]
        else:
            # Mostrar todos los datos si no se proporciona un valor de filtro
            datos_filtrados = listings.copy()

        # Mostrar los datos filtrados en la aplicación
        st.title("Explorador de Datos de Listados de Airbnb")
        st.sidebar.write("Filtrar por", variable_seleccionada)

        # Mostrar el DataFrame filtrado en la interfaz de usuario
        st.write(datos_filtrados)

    except KeyError:
        st.error(f"La variable '{variable_seleccionada}' no existe en tus datos. Verifica la selección.")
    except Exception as e:
        st.error(f"Ocurrió un error: {str(e)}")

    

    # Barra lateral para selección de rango de precios
    precio_minimo, precio_maximo = st.sidebar.slider("Seleccionar Rango de Precios", float(listings['price'].min()), float(listings['price'].max()), (float(listings['price'].min()), float(listings['price'].max())))

        # Filtrar el DataFrame según el rango de precios seleccionado
    datos_filtrados = listings[(listings['price'] >= precio_minimo) & (listings['price'] <= precio_maximo)]

        # Contar la cantidad de registros por barrio en el rango de precios seleccionado
    conteo_por_barrio = datos_filtrados['neighbourhood'].value_counts()

        # Mostrar los datos en la aplicación
    st.title("Explorador de Precios y Barrios de Listados de Airbnb")
    st.sidebar.write(f"Filtrar por Rango de Precios: {precio_minimo} a {precio_maximo}")
    st.write(conteo_por_barrio)

        # También puedes mostrar un gráfico de barras para visualizar la información
    st.bar_chart(conteo_por_barrio)
        
        # Cargar el DataFrame (reemplazar 'ruta_del_archivo.csv' con la ruta real de tu archivo CSV)
    listings_details = pd.read_csv('df_finals/listings_details.csv')

        # Barra lateral para selección de rango de accommodates
    accommodates_min, accommodates_max = st.sidebar.slider("Seleccionar Rango de Accommodates", int(listings_details['accommodates'].min()), int(listings_details['accommodates'].max()), (int(listings_details['accommodates'].min()), int(listings_details['accommodates'].max())))

        # Filtrar el DataFrame según el rango de accommodates seleccionado
    datos_filtrados = listings_details[(listings_details['accommodates'] >= accommodates_min) & (listings_details['accommodates'] <= accommodates_max)]

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
    st.title("Explorador de Accommodates y Neighborhoods de Listados de Airbnb")
    st.sidebar.write(f"Filtrar por Rango de Accommodates: {accommodates_min} a {accommodates_max}")
    st.altair_chart(bar_chart, use_container_width=True)

if __name__ == "__main__":
    main()
