import pandas as pd
import numpy as np
import os.path as path
import data_cleaning as dtc
import os as os
import wget
from zipfile import ZipFile
from glob import glob
import plotly.graph_objects as go
import plotly.express as px



def data_preparation_g0(num_rows = None):
    print("******************* STARTING DATA GATHERING g0 *******************")
    # region data_gathering
    #Descarga del dataset 0
    tidy = 0
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
        if (path.exists("data/raw_data/datos_abiertos_covid19.zip")):
            os.remove("data/raw_data/datos_abiertos_covid19.zip")

        if (path.exists("data/raw_data/graph0-RAW.csv")):
            os.remove("data/raw_data/graph0-RAW.csv")

    #endregion

    # region data_cleaning
    if(tidy == 0):
        df_g0_raw = dtc.data_cleaning_g0(df_g0_raw, "graph0-gen_data_mx.csv")
    # endregion
    print("******************* ENDING DATA GATHERING g0 *******************")
    return df_g0_raw

def data_presentation_g0(num_rows = None):
    df_g0 = pd.read_csv("data/tidy_data/graph0-gen_data_mx.csv", nrows=num_rows)
    df_g0.drop(df_g0.filter(regex="Unname"), axis=1, inplace=True)
    df_g0_sum = df_g0.groupby(['FECHA_DEF']).sum()
    dates = df_g0['FECHA_DEF'].unique()
    df = {'FECHA_DEF': dates}
    dates_df = pd.DataFrame(df)
    dates_df.sort_values(by='FECHA_DEF', inplace=True, ascending=True)
    df_g0_sum.insert(0, 'FECHA_DEF', dates_df["FECHA_DEF"].values)

    fig = go.Figure()
    fig.add_trace(go.Scatter(y=list(df_g0_sum.NEUMONIA), x=list(df_g0_sum.FECHA_DEF),
                             mode='lines',
                             name='Neumonia'
                             ))
    fig.add_trace(go.Scatter(y=list(df_g0_sum.DIABETES), x=list(df_g0_sum.FECHA_DEF),
                             mode='lines',
                             name='Diabetes'
                             ))
    fig.add_trace(go.Scatter(y=list(df_g0_sum.EPOC), x=list(df_g0_sum.FECHA_DEF),
                             mode='lines',
                             name='EPOC'
                             ))
    fig.add_trace(go.Scatter(y=list(df_g0_sum.ASMA), x=list(df_g0_sum.FECHA_DEF),
                             mode='lines',
                             name='Asma'
                             ))
    fig.add_trace(go.Scatter(y=list(df_g0_sum.INMUSUPR), x=list(df_g0_sum.FECHA_DEF),
                             mode='lines',
                             name='Inmunosupresión'
                             ))
    fig.add_trace(go.Scatter(y=list(df_g0_sum.HIPERTENSION), x=list(df_g0_sum.FECHA_DEF),
                             mode='lines',
                             name='Hipertensión'
                             ))
    fig.add_trace(go.Scatter(y=list(df_g0_sum.CARDIOVASCULAR), x=list(df_g0_sum.FECHA_DEF),
                             mode='lines',
                             name='P. Cardiovasculares'
                             ))
    fig.add_trace(go.Scatter(y=list(df_g0_sum.OBESIDAD), x=list(df_g0_sum.FECHA_DEF),
                             mode='lines',
                             name='Obesidad'
                             ))
    fig.add_trace(go.Scatter(y=list(df_g0_sum.RENAL_CRONICA), x=list(df_g0_sum.FECHA_DEF),
                             mode='lines',
                             name='P. Renales'
                             ))
    fig.add_trace(go.Scatter(y=list(df_g0_sum.TABAQUISMO), x=list(df_g0_sum.FECHA_DEF),
                             mode='lines',
                             name='Tabaquismo'
                             ))
    fig.add_trace(go.Scatter(y=list(df_g0_sum.OTRA_COM), x=list(df_g0_sum.FECHA_DEF),
                             mode='lines',
                             name='Otros'
                             ))

    fig.update_layout(
        title="Influencia de comorbilidades en decesos",
        yaxis=dict(
            title="Decesos"
        ),
        # Add range slider
        xaxis=dict(
            title="Fechas",
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

    #fig.show()
    fig.write_image('data/assets/g0/graph_g0.png')
    return fig

def data_preparation_g1(num_rows = None):
    # Data cleaning for graph 1
    df_g1_raw = pd.read_csv(
        "data/tidy_data/graph1_vaccinated_mx.csv", nrows=num_rows)
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

def data_preparation_g2(num_rows = None):
    # Data cleaning for graph 1
    df_g2_raw = pd.read_csv(
        "data/tidy_data/graph2_vaccinated_IMSS.csv", nrows = num_rows)
    # Converting the column date into date format
    df_g2_raw.date = pd.to_datetime(df_g2_raw.date)
    df_g2_raw.date = df_g2_raw.date.dt.strftime('%Y-%m-%d')

    return df_g2_raw

def data_manipulation_g2(df_g2):
    # region Data manipulation 2
    percent = []
    # Calculating the percentage of IMSS workers are vaccinated. Total workers = 437114
    for index, row in df_g2.iterrows():
        percent.insert(index, round(((row.vaccinated * 100) / 437114), 2))

    df_g2['percentage'] = percent

    # Create object figure
    fig2 = go.Figure()

    # Adding trace to graph and styling the hover window
    fig2.add_trace(go.Scatter(x=list(df_g2.date), y=list(df_g2.vaccinated),
                              mode='lines',
                              name='Personal IMSS vacunado',
                              hovertemplate=
                              '<i><b>Día</b></i>: %{x:date}<br>' +
                              '<i><b>Vacunados</b></i>: %{y:vaccinated}<br>' +
                              '<i><b>Porcentaje</b></i>: %{text}<br>',
                              text=['{}%'.format(i + 1) for i in df_g2.percentage],
                              ))

    # Set plot layoout options
    fig2.update_layout(legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=0.01,
    ))

    # Adding range slider
    fig2.update_layout(
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
    )
    #endregion

    return fig2

def data_preparation_g3(num_rows = None):
    strains = ['Alpha', 'Beta', 'Delta', 'Epsilon', 'Gamma', 'Lambda', 'Mu', 'Other']

    if os.path.isfile("data/tidy_data/graph3_strains_cleaned.csv"):
        df_strains = pd.read_csv("data/tidy_data/graph3_strains_cleaned.csv", nrows= num_rows)
    else:
        df_strains_raw = pd.read_csv("data/raw_data/graph3_strains.csv", nrows= num_rows)
        # Deleting useless columns
        df_strains_raw.pop('country')
        df_strains_raw.pop('country_code')
        df_strains_raw.pop('source')
        df_strains_raw.pop('new_cases')
        df_strains_raw.pop('number_sequenced')
        df_strains_raw.pop('percent_cases_sequenced')
        df_strains_raw.pop('valid_denominator')
        df_strains_raw.pop('percent_variant')

        # Filling empty values with 0
        df_strains_raw.number_detections_variant.fillna(0, inplace=True)
        df_strains_raw.number_sequenced_known_variant.fillna(0, inplace=True)

        # Getting unique values of year_week column
        weeks = df_strains_raw['year_week'].unique()

        records = []
        for week in weeks:
            for strain in strains:
                elems = df_strains_raw.loc[(df_strains_raw.year_week == week) & (df_strains_raw.WHO_label == strain)]
                if len(elems) != 0:
                    percentage = round(
                        ((elems.number_detections_variant.sum() * 100) / elems.number_sequenced_known_variant.sum()), 2)
                else:
                    percentage = 0
                records.append([week, strain, percentage])

        del df_strains_raw

        df_strains = pd.DataFrame(records, columns=['year_week', 'WHO_label', 'percentage'])
        df_strains.to_csv('data/tidy_data/graph3_strains_cleaned.csv')

    return df_strains

def data_manipulation_g3(df_strains):
    strains = ['Alpha', 'Beta', 'Delta', 'Epsilon', 'Gamma', 'Lambda', 'Mu', 'Other']

    # Convert week of the year into date
    df_strains.year_week = pd.to_datetime(df_strains['year_week'].astype(str) + '1', format="%Y-%W%w")

    fig3 = go.Figure()
    for elem in strains:
        strain = df_strains.query(f"WHO_label=='{elem}'")
        fig3.add_trace(go.Scatter(x=list(strain.year_week), y=list(strain.percentage),
                                  mode='lines+markers',
                                  name=f"{elem}"
                                  ))

    # Add range slider
    fig3.update_layout(
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
        hovermode='x unified'
    )

    return fig3

def data_preparation_g4(num_rows = None):
    df_efficiency = pd.read_csv("data/tidy_data/graph4_efficiency.csv", nrows=num_rows)
    return df_efficiency

def data_manipulation_g4(df_efficiency):
    fig4 = px.bar(df_efficiency, x=df_efficiency.lineage, y=df_efficiency.efficiency,
                  color=df_efficiency.brand,
                  barmode='group',
                  labels={
                      "lineage": "Cepas",
                      "efficiency": "Eficacia",
                      "brand": "Vacuna"
                  },
                  )

    fig4.update_layout(barmode='group')

    return fig4