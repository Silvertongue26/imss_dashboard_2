import dash
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Output, Input, State
import dash_table_experiments as dt
from plotly.graph_objs.layout import Margin
from dash import dcc, html
from pandas_profiling import ProfileReport
from sklearn.neighbors import LocalOutlierFactor
import sweetviz
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
import time

desired_width = 320
pd.set_option('display.width', desired_width)

def data_eda_g0(df_g0):
    print("******************* STARTING EDA g0 *******************")
    df_g0.drop(df_g0.filter(regex="Unname"), axis=1, inplace=True)
    print("Forma del dataframe: " + str(df_g0.shape))

    print("Tipo de datos: ")
    print(df_g0.dtypes)

    df_g0["SEXO"].replace({1: "Mujer", 2: "Hombre"}, inplace=True)

    df_g0_sum = df_g0.groupby(['FECHA_DEF', 'SEXO']).sum()
    #print(df_g0.groupby('FECHA_DEF').sum())
    print(df_g0_sum.head(5))
    print(df_g0_sum.columns)
    print(df_g0_sum.agg(['mean', 'min', 'max']))

    df_g0["SEXO"].replace({"Mujer":1, "Hombre":2}, inplace=True)

    #print(df_g0.groupby(df_g0['FECHA_DEF']))
    df_profile = ProfileReport(
        df_g0_sum,
        explorative=True,
        title='Comportamiento de dataframe',
        html={'style': {'full_width': False}}
    )

    df_profile.to_file("data/assets/g0/eda_g0_profile.html")

    #SV_profile = sweetviz.analyze(df_g0_sum)
    #SV_profile.show_html("data/assets/g0/eda_g0_profile_SV.html")
    print("******************* ENDING EDA g0 *******************")

