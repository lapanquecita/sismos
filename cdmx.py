"""
Este script genera un mapa con la ubicación de los sismos ocurridos dentro o cerca de la CDMX.

Los datos más nuevos se pueden obtener del siguiente enlace:

http://www2.ssn.unam.mx:8080/catalogo/

"""

import json

import pandas as pd
import plotly.graph_objects as go


def main():
    """
    Crea un mapa choropleth con los sismos registrados dentro de la CDMX.
    """

    # Cargamos el CSV de terremotos.
    df = pd.read_csv("./data.csv", parse_dates=["Fecha"], index_col="Fecha")

    # Seleccionamos registros del año 2010 en adelante.
    df = df[df.index.year >= 2010]

    # Extraemos el nombre del estado.
    df["estado"] = df["Referencia de localizacion"].apply(
        lambda x: x.split(",")[-1].strip()
    )

    # Escogemos solamente sismos ocurridos en la CDMX.
    df = df[df["estado"] == "CDMX"]

    # Filtramos sismos sin magnitud.
    df = df[df["Magnitud"] != "no calculable"]

    # Convertimos la magnitud a float.
    df["Magnitud"] = df["Magnitud"].astype(float)

    # Iniciamos el string para nuestra anotación por año.
    por_año = ["<b>Registros por año</b>"]

    # Creamos un DataFrame con los registros por año.
    df_año = df.resample("YE").count()["Magnitud"]

    # Iteramos sobre este nuevo DataFrame para crear nuestros totales por año.
    for index, row in df_año.items():
        if row == 1:
            por_año.append(f"{index.year}: {row} sismo")
        else:
            por_año.append(f"{index.year}: {row} sismos")

    # Contamos todos los sismos de nuestro DataFrame filtrado.
    subtitulo = f"{len(df)} registros totales"

    # Estas listas serán usadas para nuestro mapa Choropleth.
    ubicaciones = list()
    valores = list()

    # Cargamos el GeoJSON de la CDMX.
    geojson = json.load(open("./assets/Ciudad de México.json", "r", encoding="utf-8"))

    # Iteramos sobre las alcaldías dentro del GeoJSON.
    for item in geojson["features"]:
        geo = item["properties"]["CVEGEO"]

        # A cada alcaldía le asignamos el valor 1.
        ubicaciones.append(geo)
        valores.append(1)

    fig = go.Figure()

    # Primero creamos un mapa Choropleth donde solo se mostrarán los contornos de las alcaldías.
    fig.add_traces(
        go.Choropleth(
            geojson=geojson,
            locations=ubicaciones,
            z=valores,
            showscale=False,
            featureidkey="properties.CVEGEO",
            colorscale=["#000000", "#000000"],
            marker_line_color="#FFFFFF",
            marker_line_width=1.5,
            zmin=0.0,
            zmax=1.0,
        )
    )

    # Esta lista de listas nos ayudará a definir el color de cada grupo de sismos.
    # Así como su nombre y rango.
    bins = [
        [0, 0.99999, "#ea80fc", "< 1.0"],
        [1.0, 1.9999, "#00e5ff", "De 1.0 a 1.9"],
        [2.0, 2.9999, "#fdd835", "De 2.0 a 2.9"],
        [3.0, 10, "#FFA500", "≥ 3.0"],
    ]

    # Iteramos sobre la lista anterior y creamos un Scattergeo para cada una.
    for start, end, color, nombre in bins:
        # Creamos un DataFrame temporal con el rango de sismos.
        temp_df = df[df["Magnitud"].between(start, end)]

        # Contamos el número de sismos.
        cantidad = len(temp_df)

        fig.add_traces(
            go.Scattergeo(
                lon=temp_df["Longitud"],
                lat=temp_df["Latitud"],
                marker_color=color,
                marker_size=temp_df["Magnitud"] * 4,
                marker_line_width=2.25,
                marker_opacity=1.0,
                marker_symbol="circle-open",
                name=f"{nombre} ({cantidad} sismos)"
                if cantidad != 1
                else f"{nombre} ({cantidad} sismo)",
            )
        )

    fig.update_geos(
        fitbounds="geojson",
        projection_type="mercator",
        showocean=True,
        oceancolor="#082032",
        showcountries=False,
        framecolor="#FFFFFF",
        framewidth=2,
        showlakes=False,
        coastlinewidth=0,
        landcolor="#1A1A2E",
    )

    fig.update_layout(
        showlegend=True,
        legend_bgcolor="#16213E",
        legend_title=" <b>Magnitud del sismo</b>",
        legend_title_side="top center",
        legend_itemsizing="constant",
        legend_x=0.07,
        legend_y=0.02,
        legend_xanchor="left",
        legend_yanchor="bottom",
        legend_bordercolor="#FFFFFF",
        legend_borderwidth=1.0,
        font_family="Quicksand",
        font_color="#FFFFFF",
        font_size=18,
        margin={"r": 0, "t": 60, "l": 0, "b": 60},
        width=1280,
        height=1280,
        paper_bgcolor="#16213E",
        annotations=[
            dict(
                x=0.94,
                y=0.95,
                xanchor="right",
                yanchor="top",
                text="<br>".join(por_año),
                borderpad=10,
                bordercolor="#FFFFFF",
                borderwidth=1.0,
                bgcolor="#16213E",
                align="left",
            ),
            dict(
                x=0.5,
                y=1.015,
                xanchor="center",
                yanchor="top",
                text="Sismos registrados con epicentro cerca o dentro de la Ciudad de México (2010-2024)",
                font_size=26,
            ),
            dict(
                x=0.06,
                y=-0.039,
                xanchor="left",
                yanchor="top",
                text="Fuente: SSN (29/02/2024)",
                font_size=22,
            ),
            dict(
                x=0.5,
                y=-0.039,
                xanchor="center",
                yanchor="top",
                text=subtitulo,
                font_size=22,
            ),
            dict(
                x=0.96,
                y=-0.039,
                xanchor="right",
                yanchor="top",
                text="🧁 @lapanquecita",
                font_size=22,
            ),
        ],
    )

    fig.write_image("./cdmx.png")


if __name__ == "__main__":
    main()
