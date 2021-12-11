import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import EDA

def data_cleaning_g0(df_g0_raw,output_file):
    print("******************* STARTING DATA CLEANING g0 *******************")
    # region Data_cleaning_g0
    # Eliminamos columnas inecesarias
    #df_g0_raw.drop(df_g0_raw.filter(regex="Unname"), axis=1, inplace=True)

    df_g0_raw.pop('FECHA_ACTUALIZACION')
    df_g0_raw.pop('ID_REGISTRO')
    df_g0_raw.pop('ORIGEN')
    df_g0_raw.pop('SECTOR')
    df_g0_raw.pop('ENTIDAD_RES')
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

    # Seleccionamos información requerida y se sustituyen valores no requeridos
    df_g0_raw = df_g0_raw.loc[(df_g0_raw.FECHA_DEF != '9999-99-99') & ((df_g0_raw.CLASIFICACION_FINAL == 1 ) | (df_g0_raw.CLASIFICACION_FINAL == 2 ) | (df_g0_raw.CLASIFICACION_FINAL == 3 ) )]
    df_g0_raw.drop(df_g0_raw.filter(regex="Unname"), axis=1, inplace=True)

    df_g0_raw.assign(FECHA_DEF = pd.to_datetime(df_g0_raw.FECHA_DEF).dt.strftime('%Y-%m-%d'))

    #Revisamos y eliminamos si hay valores nulos
    if(df_g0_raw.FECHA_DEF.isnull().values.any() > 0):
        df_g0_raw.dropna(how= 'any', axis=0, subset=['FECHA_DEF'], inplace = True)

    #Buscamos y eliminamos valores duplicados
    print("Pre eliminación de duplicados: " + str(df_g0_raw.shape))
    print("Duplicados:   " + str(df_g0_raw.duplicated().sum()))
    df_g0_raw.drop_duplicates(
        subset=['SEXO', 'FECHA_DEF', 'NEUMONIA', 'EDAD', 'DIABETES', 'EPOC', 'ASMA', 'INMUSUPR',
                'HIPERTENSION', 'OTRA_COM', 'CARDIOVASCULAR', 'OBESIDAD', 'RENAL_CRONICA', 'TABAQUISMO',
                'CLASIFICACION_FINAL'], keep="first", inplace=True)
    print("Pos eliminación de duplicados: " + str(df_g0_raw.shape))

    #Guardamos el dataframe limpio
    df_g0_raw.to_csv("data/tidy_data/"+output_file)
    print("******************* ENDING DATA CLEANING g0 *******************")
    return df_g0_raw
    #endregion

def outlier_detection_g0(df_g0):
    print("******************* STARTING OUTLIERS g0 *******************")
    g = sns.pairplot(df_g0, x_vars=["EDAD", "CLASIFICACION_FINAL"],
                     y_vars=["EDAD", "CLASIFICACION_FINAL"], corner=True,  diag_kind="kde"
                 )
    g.map_lower(sns.kdeplot, levels=4, color=".2")
    #plt.show()
    plt.savefig('data/assets/g0/pairplot.png')
    print("******************* ENDING OUTLIERS g0 *******************")

def data_cleaning_g1(df_g1_raw,output_file):
    return 1