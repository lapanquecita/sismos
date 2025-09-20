"""

Este script genera un sencillo mapa de densidad con todos los sismos registrados en México.
Solo se considera la frencuencia, no la magnitud.
El propósito del mapa es meramente ilustrativo.

"""

import json

import pandas as pd
import plotly.graph_objects as go


def main():
    """
    Genera un mapa de densidad con todos los sismos registrados en México.
    """

    # Cargamos el dataset de sismos.
    df = pd.read_csv("./data.csv", parse_dates=["Fecha"])

    # El subtitulo dirá el número de sismos registrados.
    subtitulo = f"<b>{len(df):,.0f}</b> sismos registrados"

    # Cargamos el GeoJSON de México.
    geojson = json.loads(open("./assets/mexico.json", "r", encoding="utf-8").read())

    # En un mapa de densidad los valores son comunmente del 0 al 1.
    # Creamos las marcas y etiquetas manualmente.
    marcas = [0.0, 0.25, 0.5, 0.75, 1.0]
    etiquetas = ["Muy baja", "Baja", "Moderada", "Alta", "Muy alta"]

    fig = go.Figure()

    # Creamos la capa del mapa de densidad.
    fig.add_traces(
        go.Densitymap(
            lat=df["Latitud"],
            lon=df["Longitud"],
            radius=1.75,
            colorscale="YlOrRd_r",
            colorbar=dict(
                x=0.035,
                y=0.5,
                thickness=150,
                ypad=400,
                ticks="outside",
                outlinewidth=5,
                outlinecolor="#FFFFFF",
                tickvals=marcas,
                ticktext=etiquetas,
                tickwidth=5,
                tickcolor="#FFFFFF",
                ticklen=30,
                tickfont_size=80,
            ),
        )
    )

    # Creamos la capa de la división política estatal.
    fig.add_traces(
        go.Choroplethmap(
            geojson=geojson,
            locations=[f"{i:02}" for i in range(1, 33)],
            z=[1 for _ in range(32)],
            featureidkey="properties.CVEGEO",
            colorscale=["hsla(0, 0, 0, 0)", "hsla(0, 0, 0, 0)"],
            marker_line_color="#FFFFFF",
            marker_line_width=3,
            showscale=False,
            below="",
        )
    )

    # Vamos a crear un borde para el mapa.
    # El borde es un rectángulo con fondo transparente.
    fig.add_shape(
        type="rect",
        x0=0,
        y0=0,
        x1=1,
        y1=1,
        line_color="#FFFFFF",
        line_width=5,
        fillcolor="rgba(0,0,0,0)",
    )

    # Personalizamos el mapa.
    fig.update_layout(
        map_center_lat=24,
        map_center_lon=-102,
        map_zoom=6.8,
        map_style="carto-darkmatter-nolabels",
        showlegend=False,
        font_family="Inter",
        font_color="#FFFFFF",
        font_size=120,
        margin_t=260,
        margin_r=100,
        margin_b=220,
        margin_l=100,
        width=7680,
        height=4320,
        paper_bgcolor="#2B2B2B",
        annotations=[
            dict(
                x=0.98,
                y=0.95,
                xanchor="right",
                yanchor="top",
                text="<b>Nota:</b><br>No se considera la magnitud de los sismos<br>sino su frecuencia en la misma región.",
                align="left",
                borderpad=30,
                bordercolor="#FFFFFF",
                bgcolor="#000000",
                borderwidth=5,
            ),
            dict(
                x=0.5,
                y=1.05,
                xanchor="center",
                yanchor="top",
                text="Distribución de epicentros de todos los sismos registrados en México (1900-2025)",
                font_size=140,
            ),
            dict(
                x=0.02,
                y=0.49,
                textangle=-90,
                xanchor="center",
                yanchor="middle",
                text="Frecuencia relativa",
                font_size=100,
            ),
            dict(
                x=0,
                y=-0.06,
                xanchor="left",
                yanchor="bottom",
                text="Fuente: SSN (19/09/2025)",
            ),
            dict(
                x=0.5,
                y=-0.06,
                xanchor="center",
                yanchor="bottom",
                text=subtitulo,
            ),
            dict(
                x=1.0,
                y=-0.06,
                xanchor="right",
                yanchor="bottom",
                text="🧁 @lapanquecita",
            ),
        ],
    )

    fig.write_image("./mapa_densidad.png")


if __name__ == "__main__":
    main()
