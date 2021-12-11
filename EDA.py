import pandas as pd
from pandas_profiling import ProfileReport
import sweetviz
import seaborn as sns
import matplotlib.pyplot as plt

desired_width = 320
pd.set_option('display.width', desired_width)

def data_eda_g0(df_g0):
    print("******************* STARTING EDA g0 *******************")
    df_g0.drop(df_g0.filter(regex="Unname"), axis=1, inplace=True)
    pd.set_option("display.max_rows", None, "display.max_columns", None)

    print("Forma del dataframe: " + str(df_g0.shape))

    print("Tipo de datos: ")
    print(df_g0.dtypes)

    print("Descripción: ")
    print(df_g0.describe())

    df_g0["SEXO"].replace({1: "Mujer", 2: "Hombre"}, inplace=True)

    df_g0_sum = df_g0.groupby(['FECHA_DEF', 'SEXO']).sum()

    print(df_g0.groupby('FECHA_DEF').sum())
    print(df_g0_sum.head(10))
    #print(df_g0_sum.columns)
    print(df_g0_sum.agg(['mean', 'min', 'max']))

    df_g0["SEXO"].replace({"Mujer":1, "Hombre":2}, inplace=True)

    plt.figure(figsize=(15, 6))
    sns.set(font_scale=.8)
    hm = sns.heatmap(df_g0.corr(), vmin=-1, vmax=1, annot=True, cmap='PiYG')
    hm.set_title('Correlation Heatmap', fontdict={'fontsize': 15})
    plt.savefig('data/assets/g0/heatmap.png')

    #print(df_g0.groupby(df_g0['FECHA_DEF']))
    df_profile = ProfileReport(
        df_g0,
        explorative=True,
        title='Comportamiento de dataframe',
        html={'style': {'full_width': False}}
    )

    df_profile.to_file("data/assets/g0/eda_g0_profile.html")

    SV_profile = sweetviz.analyze(df_g0_sum)
    SV_profile.show_html("data/assets/g0/eda_g0_profile_SV.html")
    print("******************* ENDING EDA g0 *******************")

