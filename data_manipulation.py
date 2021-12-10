import pandas as pd
import numpy as np
import os.path as path
import os as os
import wget
from zipfile import ZipFile
from glob import glob
import plotly.express as px
import plotly.graph_objects as go

###OLD NOT TO USE
def data_preparation_g0(num_rows = None):
    # region data_gathering
    #Descarga del dataset 0
    if(path.exists("data/raw_data/graph0-RAW.csv") == False):
        wget.download('https://datosabiertos.salud.gob.mx/gobmx/salud/datos_abiertos/datos_abiertos_covid19.zip', "data/raw_data" )
        with ZipFile("data/raw_data/datos_abiertos_covid19.zip", 'r') as zip:
            #Muestra los contenidos del archivo zip
            zip.printdir()
            #Se extraen los documentos
            print('Extracting all the files now...')
            zip.extractall("data/raw_data")
            print('Done!')

        filename = glob("data/raw_data/*COVID19MEXICO.csv")[0]
        os.rename(filename, "data/raw_data/graph0-RAW.csv")

        df_g0_raw = pd.read_csv("data/raw_data/graph0-RAW.csv", nrows=100)

    else:
        df_g0_raw = pd.read_csv(
            "data/raw_data/graph0-RAW.csv", nrows=num_rows)
        # Se eliminan los documentos extras para reducir espacio
        #ACTUALIZAR
        #if (path.exists("data/raw_data/datos_abiertos_covid19.zip")):
            #os.remove("data/raw_data/datos_abiertos_covid19.zip")

        #if (path.exists("data/raw_data/graph0-RAW.csv")):
            #os.remove("data/raw_data/graph0-RAW.csv")

    #endregion

    # region data_cleaning
    #Eliminamos columnas inecesarias
    df_g0_raw.pop('FECHA_ACTUALIZACION')
    df_g0_raw.pop('ID_REGISTRO')
    df_g0_raw.pop('ORIGEN')
    df_g0_raw.pop('SECTOR')
    df_g0_raw.pop('ENTIDAD_UM')
    df_g0_raw.pop('ENTIDAD_NAC')
    df_g0_raw.pop('MUNICIPIO_RES')
    df_g0_raw.pop('HABLA_LENGUA_INDIG')
    df_g0_raw.pop('INDIGENA')
    df_g0_raw.pop('NACIONALIDAD')
    df_g0_raw.pop('EMBARAZO')
    df_g0_raw.pop('OTRO_CASO')
    df_g0_raw.pop('TOMA_MUESTRA_LAB')
    df_g0_raw.pop('INTUBADO')
    df_g0_raw.pop('TIPO_PACIENTE')
    df_g0_raw.pop('RESULTADO_LAB')
    df_g0_raw.pop('TOMA_MUESTRA_ANTIGENO')
    df_g0_raw.pop('RESULTADO_ANTIGENO')
    df_g0_raw.pop('MIGRANTE')
    df_g0_raw.pop('PAIS_NACIONALIDAD')
    df_g0_raw.pop('PAIS_ORIGEN')
    df_g0_raw.pop('UCI')
    df_g0_raw.pop('FECHA_INGRESO')
    df_g0_raw.pop('FECHA_SINTOMAS')
    # endregion

    return df_g0_raw

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