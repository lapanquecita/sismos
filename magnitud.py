import pandas as pd
import plotly.graph_objects as go
from PIL import Image

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


def plot_magnitud(low, high, archivo):
    """
    Crea una gráfica de barras con el número de sismos ocurridos por mes.

    Parameters
    ----------
    low : int
        La magnitud mínimadel sismo.

    high : int
        La magnitud máxima del sismo.

    archivo : int
        El nombre del archivo a guardar.
    """

    # Cargamos el dataset de sismos.
    df = pd.read_csv("./data.csv", parse_dates=["Fecha"], index_col="Fecha")

    # Quitamos sismos sin magnitud.
    df = df[df["Magnitud"] != "no calculable"]

    # Convertimos el resto de magnitudes a float.
    df["Magnitud"] = df["Magnitud"].astype(float)

    # Filtramos por magnitud.
    df = df[df["Magnitud"].between(low, high)]

    # Creamos una columna para el mes de ocurrencia.
    df["mes"] = df.index.month

    # Creamos un DataFrame esqueleto para los registros por mes.
    # Esto para siempre tener 12 columnas, una por mes.
    meses_df = pd.DataFrame({"total": [0] * 12}, index=range(1, 13))

    # Actualizamos los valores del esqueleto con los valores reales.
    meses_df.update(df["mes"].value_counts().to_frame("total"))

    # Preparamos los textos para cada barra.
    meses_df["perc"] = meses_df["total"] / meses_df["total"].sum() * 100
    meses_df["text"] = meses_df.apply(
        lambda x: f"<b>{x['total']:,.0f}</b><br>({x['perc']:,.1f}%)".replace(
            ".0%", "%"
        ),
        axis=1,
    )

    # Agregamos el nombre del mes.
    meses_df.index = meses_df.index.map(MESES)

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=meses_df.index,
            y=meses_df["total"],
            text=meses_df["text"],
            marker_color=meses_df["total"],
            name=f"Total de registros: <b>{meses_df['total'].sum():,.0f}</b>",
            textfont_size=32,
            marker_line_width=0,
            marker_colorscale="portland",
            textposition="outside",
        )
    )

    fig.update_xaxes(
        ticks="outside",
        ticklen=10,
        zeroline=False,
        tickcolor="#FFFFFF",
        linewidth=2,
        showgrid=False,
        gridwidth=0.5,
        showline=True,
        mirror=True,
    )

    fig.update_yaxes(
        title="Número de registros (% del total)",
        range=[0, meses_df["total"].max() * 1.12],
        ticks="outside",
        ticklen=10,
        title_standoff=15,
        tickcolor="#FFFFFF",
        linewidth=2,
        showgrid=True,
        gridwidth=0.5,
        showline=True,
        mirror=True,
        nticks=20,
    )

    fig.update_layout(
        showlegend=True,
        legend_xanchor="left",
        legend_yanchor="top",
        legend_x=0.01,
        legend_y=0.98,
        legend_borderwidth=1,
        legend_bordercolor="#FFFFFF",
        width=1920,
        height=1080,
        font_family="Inter",
        font_color="#FFFFFF",
        font_size=24,
        title_text=f"Eventos sísmicos de magnitud <b>{low}-{high}</b> registrados en México (1900-2025)",
        title_x=0.5,
        title_y=0.965,
        margin_t=80,
        margin_l=140,
        margin_r=40,
        margin_b=120,
        title_font_size=36,
        plot_bgcolor="#1E1E1E",
        paper_bgcolor="#20252f",
        annotations=[
            dict(
                x=0.015,
                y=-0.11,
                xref="paper",
                yref="paper",
                xanchor="left",
                yanchor="top",
                text="Fuente: SSN (01/09/2025)",
            ),
            dict(
                x=0.5,
                y=-0.11,
                xref="paper",
                yref="paper",
                xanchor="center",
                yanchor="top",
                text="Mes de ocurrencia",
            ),
            dict(
                x=1.01,
                y=-0.11,
                xref="paper",
                yref="paper",
                xanchor="right",
                yanchor="top",
                text="🧁 @lapanquecita",
            ),
        ],
    )

    fig.write_image(f"./{archivo}.png")


def combine_images():
    """
    Combina todas las imágenes creadas en la función anterior.
    """

    image1 = Image.open("./1.png")
    image2 = Image.open("./2.png")
    image3 = Image.open("./3.png")
    image4 = Image.open("./4.png")

    result_width = image1.width
    result_height = image1.height + image2.height + image3.height + image4.height

    result = Image.new("RGB", (result_width, result_height))
    result.paste(im=image1, box=(0, 0))
    result.paste(im=image2, box=(0, image1.height))
    result.paste(im=image3, box=(0, image1.height + image2.height))
    result.paste(im=image4, box=(0, image1.height + image2.height + image3.height))

    result.save("./final.png")


if __name__ == "__main__":
    plot_magnitud(5.0, 5.9, 1)
    plot_magnitud(6.0, 6.9, 2)
    plot_magnitud(7.0, 7.9, 3)
    plot_magnitud(8.0, 8.9, 4)

    combine_images()
