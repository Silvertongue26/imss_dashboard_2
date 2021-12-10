import pandas as pd
import numpy as np
import os.path as path
import data_cleaning as dtc
import os as os
import wget
from zipfile import ZipFile
from glob import glob
import plotly.graph_objects as go


def data_preparation_g0(num_rows = None):
    print("******************* STARTING DATA GATHERING g0 *******************")
    # region data_gathering
    #Descarga del dataset 0
    tidy = 0
    if(path.exists("data/raw_data/graph0-RAW.csv") == False):
        #wget.download('https://datosabiertos.salud.gob.mx/gobmx/salud/datos_abiertos/datos_abiertos_covid19.zip', "data/raw_data" )
        with ZipFile("data/raw_data/datos_abiertos_covid19.zip", 'r') as zip:
            #Muestra los contenidos del archivo zip
            zip.printdir()
            #Se extraen los documentos
            print('Extracting all the files now...')
            zip.extractall("data/raw_data")
            print('Done!')

        filename = glob("data/raw_data/*COVID19MEXICO.csv")[0]
        os.rename(filename, "data/raw_data/graph0-RAW.csv")
        df_g0_raw = pd.read_csv("data/raw_data/graph0-RAW.csv", nrows=num_rows)

    else:
        if(path.exists("data/tidy_data/graph0-gen_data_mx.csv")):
            route = "data/tidy_data/graph0-gen_data_mx.csv"
            tidy = 1
        else:
            route = "data/raw_data/graph0-RAW.csv"
            tidy = 0

        df_g0_raw = pd.read_csv(
            route, nrows=num_rows)

        # Se eliminan los documentos extras para reducir espacio
        """if (path.exists("data/raw_data/datos_abiertos_covid19.zip")):
            os.remove("data/raw_data/datos_abiertos_covid19.zip")

        if (path.exists("data/raw_data/graph0-RAW.csv")):
            os.remove("data/raw_data/graph0-RAW.csv")"""

    #endregion

    # region data_cleaning
    if(tidy == 0):
        df_g0_raw = dtc.data_cleaning_g0(df_g0_raw, "graph0-gen_data_mx.csv")
    # endregion
    print("******************* ENDING DATA GATHERING g0 *******************")
    return df_g0_raw


def data_preparation_g1(num_row = None):
    # Data cleaning for graph 1
    df_g1_raw = pd.read_csv(
        "https://raw.githubusercontent.com/Silvertongue26/imss_dashboard/main/data/graph1_vaccinated_mx.csv")
    # Elimination of useless columns
    df_g1_raw.pop('location')
    df_g1_raw.pop('vaccine')
    df_g1_raw.pop('total_vaccinations')
    df_g1_raw.pop('total_boosters')
    df_g1_raw.pop('source_url')

    return df_g1_raw

def data_manipulation_g1(df_g1):
    # region Data manipulation 1
    # Data cleaning for graph 1
    df_g1 = pd.read_csv(
        "https://raw.githubusercontent.com/Silvertongue26/imss_dashboard/main/data/graph1_vaccinated_mx.csv")
    # Elimination of useless columns
    df_g1.pop('location')
    df_g1.pop('vaccine')
    df_g1.pop('total_vaccinations')
    df_g1.pop('total_boosters')
    df_g1.pop('source_url')

    # Create figure object
    fig = go.Figure()

    # Adding trace for total vaccinated
    fig.add_trace(go.Scatter(x=list(df_g1.date), y=list(df_g1.people_vaccinated),
                             mode='lines',
                             name='Total de vacunados'
                             ))
    # Adding trace for people with 2 vaccines on
    fig.add_trace(go.Scatter(x=list(df_g1.date), y=list(df_g1.people_fully_vaccinated),
                             mode='lines',
                             name='Esquemas completos'
                             ))

    # Set plot layout options for displaying keys inside graph
    fig.update_layout(
        legend=dict(
            # title_text="Avance de vacunación en México"
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        ),
        # Add range slider
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(
                        count=1,
                        label="Último mes",
                        step="month",
                        stepmode="backward"
                    ),
                    dict(
                        count=6,
                        label="Últimos 6 meses",
                        step="month",
                        stepmode="backward"
                    ),
                    dict(count=1,
                         label="Último año",
                         step="year",
                         stepmode="backward"
                         ),
                    dict(
                        count=1,
                        label="Todo",
                        step="all"
                    )
                ])
            ),
            rangeslider=dict(visible=True),
            type="date"
        ),
        hovermode='x'
    )
    #endregion

    return fig