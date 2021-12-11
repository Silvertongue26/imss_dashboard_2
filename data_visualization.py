import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
import plotly.express as px

def data_visualization_g0(df_g0):
    print("******************* STARTING DV g0 *******************")

    #Eliminamos columna de fecha porque no se ocupara en esta situación
    df_g0.pop('FECHA_DEF')
    n_components = 6
    pca = PCA(n_components = n_components)
    pca.fit(df_g0)

    # region pca_1
    """
    X_pca = pca.transform(df_g0)
    print("original shape:   ", df_g0.shape)
    print("transformed shape:", X_pca.shape)
    X_new = pca.inverse_transform(X_pca)
    plt.scatter(df_g0.iloc[:, 3], df_g0.iloc[:, 14], alpha=0.2)
    plt.scatter(X_new[:, 3], X_new[:, 14], alpha=0.8)
    plt.axis('equal')
    plt.savefig("data/assets/g0/pca_1.png")
    print("PCA 1 FINISHED")
    """
    #endregion

    # region pca_2
    plt.xlim([0, 10])
    plt.ylim([0, 4])
    plt.yticks(np.arange(-4, 4, 1))
    plt.xticks(np.arange(10, 10, 1))
    plt.scatter(df_g0.iloc[:, 3], df_g0.iloc[:, 14],
                c=df_g0.CLASIFICACION_FINAL, edgecolor='none', alpha=0.5,
                cmap=plt.cm.get_cmap('BuGn_r', 10))
    plt.xlabel('EDAD')
    plt.ylabel('CLASIFICACION_FINAL')
    plt.colorbar()
    plt.savefig("data/assets/g0/pca_2.png")
    print("PCA 2 FINISHED")
    # endregion

    # region pca_3
    """
    plt.plot(np.cumsum(pca.explained_variance_ratio_))
    plt.xlabel('number of components')
    plt.ylabel('cumulative explained variance')
    plt.savefig("data/assets/g0/pca_3.png")
    print("PCA 3 FINISHED")
    """
    # endregion

    # region pca_4
    pd.DataFrame(
        np.transpose(pca.components_),
        columns=[f'PC {x}' for x in range(1, n_components + 1)]
    )
    print(pca.explained_variance_)

    df_ev = pd.DataFrame({
        "acc": np.cumsum(pca.explained_variance_ratio_),
        "label": [f'PC {x}' for x in range(1, n_components + 1)]
    })
    fig = px.scatter(df_ev, x='label', y='acc')
    fig.write_image('data/assets/g0/pca_4.png')
    print("PCA 4 FINISHED")
    # endregion

    # region pca_5
    fig = px.bar(df_g0, x='EDAD', y='CLASIFICACION_FINAL', text='EDAD', color="CLASIFICACION_FINAL")
    fig.write_image('data/assets/g0/pca_5.png')
    print("PCA 5 FINISHED")
    # endregion
    print("******************* ENDING DV g0 *******************")
