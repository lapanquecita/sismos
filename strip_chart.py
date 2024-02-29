"""
Este programa crea una gráfica de puntos, la cual es ideal para
mostrar la distribución completa de una muestra.

Los datos más nuevos se pueden obtener del siguiente enlace:

http://www2.ssn.unam.mx:8080/catalogo/

"""

import numpy as np
import pandas as pd
import plotly.graph_objects as go

# Este diccionario será utilizado para nuestras
# etiquetas del eje horizontal.
MESES = {
    1: "Ene.",
    2: "Feb.",
    3: "Mar.",
    4: "Abr.",
    5: "May.",
    6: "Jun.",
    7: "Jul.",
    8: "Ago.",
    9: "Sep.",
    10: "Oct.",
    11: "Nov.",
    12: "Dic.",
}


def main():
    # Creamos 12 tonos de colores tipo hsla, con 100% de saturación
    # 75% de iluminación y 90% de transparencia.
    tonos_de_color = [f"hsla({h}, 100%, 75%, 1.0)" for h in np.linspace(0, 360, 12)]

    # Cargamos nuestro dataset de sismos.
    df = pd.read_csv("./data.csv", parse_dates=["Fecha"], index_col="Fecha")

    # Filtramos todos los sismos sin magnitud.
    df = df[df["Magnitud"] != "no calculable"].copy()

    # Convertimos las magnitudes a float.
    df["Magnitud"] = df["Magnitud"].astype(float)

    # Seleccionamos sismos de magnitud 6.0 o superior.
    df = df[df["Magnitud"] >= 6.0]

    fig = go.Figure()

    # Vamor a iterar sobre todos los meses y extraer los sismos correspondientes.
    for numero, mes in MESES.items():
        # Seleccionamos todos los sismos del mes correspondiente.
        temp_df = df[df.index.month == numero]

        # Vamos a crear la etiqueta para el eje horizontal.
        # Esta etiqueta es la misma cadena de caracteres repetida el 'numero
        # de veces igual al largo del DataFrame del mes correspondiente.
        etiquetas = [f"{mes} ({len(temp_df)})" for _ in range(len(temp_df))]

        # Las magnitudes son extraídas de la columna y convertidas a una lista.
        magnitudes = temp_df["Magnitud"].tolist()

        # Para crear una gráfica de puntos debemos modificar una de tipo Box.
        # Lo que hacemos es mostrar todos los puntitos, hacer invisibles los bigotes
        # y las cajas.
        # Los dos parámetros más importantes boxpoints y pointpos, los cuales
        # nos permiten mostrar todos los puntos y centrarlos donde iban las cajas.
        # Al final seleccionamos el tono de color correspondiente al mes.
        fig.add_traces(
            go.Box(
                x=etiquetas,
                y=magnitudes,
                boxpoints="all",
                pointpos=0,
                whiskerwidth=0,
                line_width=0,
                fillcolor="hsla(0, 0, 0, 0)",
                jitter=1,
                marker_size=14,
                marker_color=tonos_de_color[-numero],
                marker_symbol="circle-open",
                marker_line_width=2.5,
            )
        )

    fig.update_xaxes(
        ticks="outside",
        ticklen=10,
        tickfont_size=14,
        title_standoff=18,
        tickcolor="#FFFFFF",
        linewidth=2,
        gridwidth=0.0,
        showline=True,
        mirror=True,
    )

    fig.update_yaxes(
        title="Magnitud del sismo",
        range=[5.8, 8.4],
        ticks="outside",
        tickfont_size=14,
        ticklen=10,
        title_standoff=6,
        tickcolor="#FFFFFF",
        linewidth=2,
        gridwidth=0.5,
        showline=True,
        mirror=True,
        nticks=20,
    )

    fig.update_layout(
        showlegend=False,
        width=1280,
        height=720,
        font_family="Quicksand",
        font_color="white",
        font_size=18,
        title_text="Distribución de eventos sísmicos de <b>magnitud ≥ 6.0</b> por mes de ocurrencia en México (1900-2024)",
        title_x=0.5,
        title_y=0.965,
        margin_t=60,
        margin_l=100,
        margin_r=40,
        margin_b=90,
        title_font_size=24,
        plot_bgcolor="#20252f",
        paper_bgcolor="#1E1E1E",
        annotations=[
            dict(
                x=0.015,
                y=-0.13,
                xref="paper",
                yref="paper",
                xanchor="left",
                yanchor="top",
                text="Fuente: SSN (29/02/2024)",
            ),
            dict(
                x=0.5,
                y=-0.13,
                xref="paper",
                yref="paper",
                xanchor="center",
                yanchor="top",
                text="Mes de ocurrencia (total de registros)",
            ),
            dict(
                x=1.01,
                y=-0.13,
                xref="paper",
                yref="paper",
                xanchor="right",
                yanchor="top",
                text="🧁 @lapanquecita",
            ),
        ],
    )

    fig.write_image("./strip_chart.png")


if __name__ == "__main__":
    main()
