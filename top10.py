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
    df["estado"] = df["Referencia de localizacion"].apply(
        lambda x: x.split(",")[-1].strip())

    fig = go.Figure()

    # iteramos sobre los años que nos interesan.
    for año in range(2011, 2024):

        # Creamos un DataFrame con el año correspondiente
        # ordenamos las magnitudes de mayor a menor y seleccionamos
        # solo las primeras 10.
        temp_df = df[df.index.year == año].sort_values(
            "Magnitud", ascending=False)[:10]

        # Reseteamos el índice para que sea un valor del 0 al 9.
        temp_df.reset_index(inplace=True)

        # Aquí creamos el texto para los círculos usando el nombre del estado extráido previamente.
        # así como la magnitud y la fecha.
        temp_df["text"] = temp_df.apply(
            lambda x: f"{x['Magnitud']:,}<br><b>{x['estado']}</b><br>{x['Fecha']:%d/%m}", axis=1)

        # Aquí definimos el color de cada círculo usando el diccionario de colores.
        temp_df["color"] = temp_df["estado"].map(COLORES)

        # El eje vertical va a ser el año 8 veces.
        # Esto es como un hack para que nuestra visualización funcione.
        y = [f"{año:.0f}" for _ in range(10)]

        fig.add_trace(
            go.Scatter(
                x=temp_df.index,
                y=y,
                mode="markers+text",
                text=temp_df["text"],
                marker_color=temp_df["color"],
                marker_size=96,
                textfont_size=20,
                textfont_family="Oswald",
            )
        )

    fig.update_xaxes(
        range=[-0.6, 9.6],
        showticklabels=False,
        ticklen=10,
        zeroline=False,
        linewidth=2,
        showline=True,
        mirror=True,
        showgrid=False,
    )

    fig.update_yaxes(
        title="Año del evento sísmico",
        title_font_size=28,
        range=[-0.6, 12.6],
        ticks="outside",
        ticklen=10,
        zeroline=False,
        title_standoff=12,
        tickcolor="#FFFFFF",
        linewidth=2,
        showline=True,
        mirror=True,
        showgrid=False,
    )

    fig.update_layout(
        showlegend=False,
        width=1280,
        height=1600,
        font_family="Quicksand",
        font_color="#FFFFFF",
        font_size=18,
        title_text="Los 10 eventos sísmicos con mayor magnitud<br>registrados en México por año (2011-2023)",
        title_x=0.5,
        title_y=0.97,
        margin_t=120,
        margin_l=140,
        margin_r=40,
        margin_b=55,
        title_font_size=30,
        plot_bgcolor="#331D2C",
        paper_bgcolor="#331D2C",
        annotations=[
            dict(
                x=0.01,
                xanchor="left",
                xref="paper",
                y=-0.05,
                yanchor="bottom",
                yref="paper",
                text="Fuente: SSN (28/07/2023)"
            ),
            dict(
                x=0.5,
                xanchor="center",
                xref="paper",
                y=-0.05,
                yanchor="bottom",
                yref="paper",
                text="Magnitud, ubicación y fecha de ocurrencia"
            ),
            dict(
                x=1.01,
                xanchor="right",
                xref="paper",
                y=-0.05,
                yanchor="bottom",
                yref="paper",
                text="🧁 @lapanquecita"
            )
        ]
    )

    fig.write_image("./top10.png")


if __name__ == "__main__":

    main()
