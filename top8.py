"""
Este programa crea una gráfica de círculos, la cual es muy parecida
a una tabla convencional pero más estilizada.

Los datos más nuevos se pueden obtener del siguiente enlace:

http://www2.ssn.unam.mx:8080/catalogo/
"""

import pandas as pd
import plotly.graph_objects as go


# Este diccionario será utilizado para asignar colores
# a cada estado de la república.
COLORES = {
    "AGS": "#f44336",
    "BC": "#d50000",
    "BCS": "#455a64",
    "CAMP": "#e91e63",
    "COAH": "#c51162",
    "COL": "#880e4f",
    "CHIS": "#9c27b0",
    "CHIH": "#4a148c",
    "CDMX": "#aa00ff",
    "DGO": "#d500f9",
    "GTO": "#673ab7",
    "GRO": "#6200ea",
    "HGO": "#311b92",
    "JAL": "#3f51b5",
    "MEX": "#304ffe",
    "MICH": "#1a237e",
    "MOR": "#0d47a1",
    "NAY": "#1976d2",
    "NL": "#00838f",
    "OAX": "#00796b",
    "PUE": "#004d40",
    "QRO": "#616161",
    "QR": "#d32f2f",
    "SLP": "#4e342e",
    "SIN": "#795548",
    "SON": "#ff3d00",
    "TAB": "#ef6c00",
    "TAMS": "#827717",
    "TLAX": "#689f38",
    "VER": "#33691e",
    "YUC": "#388e3c",
    "ZAC": "#1b5e20",
}


def main():

    # Cargamos nuestro dataset de sismos.
    df = pd.read_csv("./data.csv", parse_dates=["Fecha"], index_col="Fecha")

    # Filtramos todos los sismos sin magnitud.
    df = df[df["Magnitud"] != "no calculable"].copy()

    # Convertimos las magnitudes a float.
    df["Magnitud"] = df["Magnitud"].astype(float)

    # Extraemos el estado donde ocurrió cada sismo usando una función personalizada.
    df["estado"] = df["Referencia de localizacion"].apply(extraer_estado)

    fig = go.Figure()

    # iteramos sobre los años que nos interesan.
    for año in range(2007, 2023):

        # Creamos un DataFrame con el año correspondiente
        # ordenamos las magnitudes de mayor a menor y seleccionamos
        # solo las primeras 8.
        temp_df = df[df.index.year == año].sort_values(
            "Magnitud", ascending=False)[:8]

        # Reseteamos el índice para que sea un valor del 0 al 7.
        temp_df.reset_index(inplace=True)

        # Aquí creamos el texto para los círculos usando el nombre del estado extráido previamente.
        # así como la magnitud y la fecha.
        temp_df["text"] = temp_df.apply(
            lambda x: "{:,}<br><b>{}</b><br>{:%d-%m}".format(x["Magnitud"], x["estado"], x["Fecha"]), axis=1)

        # Aquí definimos el color de cada círculo usando el diccionario de colores.
        temp_df["color"] = temp_df["estado"].map(COLORES)

        # El eje vertical va a ser el año 8 veces.
        # Esto es como un hack para que nuestra visualización funcione.
        y = [f"{año:.0f}" for _ in range(8)]

        fig.add_trace(
            go.Scatter(
                x=temp_df.index,
                y=y,
                mode="markers+text",
                text=temp_df["text"],
                marker_color=temp_df["color"],
                textfont_size=18,
                marker_size=90,
            )
        )

    fig.update_xaxes(
        title="",
        range=[-0.75, 7.75],
        showticklabels=False,
        ticklen=10,
        zeroline=False,
        title_standoff=20,
        tickcolor="#FFFFFF",
        linewidth=2,
        showline=True,
        mirror=True,
        showgrid=False,
        nticks=0
    )

    fig.update_yaxes(
        title="Año del evento sísmico",
        range=[-0.75, 15.75],
        ticks="outside",
        ticklen=10,
        zeroline=False,
        title_standoff=12,
        tickcolor="#FFFFFF",
        linewidth=2,
        showline=True,
        mirror=True,
        showgrid=False,
        nticks=0
    )

    fig.update_layout(
        showlegend=False,
        width=1080,
        height=1920,
        font_family="Quicksand",
        font_color="white",
        font_size=18,
        title_text="Los eventos sísmicos con mayor magnitud registrados en México del 2007 al 2022",
        title_x=0.5,
        title_y=0.98,
        margin_t=80,
        margin_l=120,
        margin_r=40,
        margin_b=60,
        title_font_size=26,
        plot_bgcolor="#0F0E0E",
        paper_bgcolor="#541212",
        annotations=[
            dict(
                x=0.01,
                xanchor="left",
                xref="paper",
                y=-0.045,
                yanchor="bottom",
                yref="paper",
                text="Fuente: SSN"
            ),
            dict(
                x=0.5,
                xanchor="center",
                xref="paper",
                y=-0.045,
                yanchor="bottom",
                yref="paper",
                text="Magnitud, ubicación y fecha de ocurrencia"
            ),
            dict(
                x=1.01,
                xanchor="right",
                xref="paper",
                y=-0.045,
                yanchor="bottom",
                yref="paper",
                text="🧁 @lapanquecita"
            )
        ]
    )

    fig.write_image("./2.png")


def extraer_estado(x):
    # El nombre del estado siempre se encuentra después de la última coma
    # sin embargo, a veces tiene espacios en blanco, entonces usamos
    # el método strip() para limpiarlo.
    return x.split(",")[-1].strip()


if __name__ == "__main__":

    main()
