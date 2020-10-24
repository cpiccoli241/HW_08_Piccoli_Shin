import matplotlib.pyplot as plt
from scipy.cluster import hierarchy
from agglomerative_cluster import cluster
from HW_08_Agglomeration_Piccoli_Shin import  remove_id
import pandas as pd

def test():
    shoping_cart_data = pd.read_csv('HW_PCA_SHOPPING_CART_v896', index_col=False, error_bad_lines=False, skipinitialspace=True)
    pd.set_option('display.max_rows', None, 'display.max_columns', None)
    shoping_cart_data = remove_id(shoping_cart_data)

    Z = hierarchy.linkage(shoping_cart_data.to_numpy(), )
    plt.figure()
    dn = hierarchy.dendrogram(Z)

    hierarchy.set_link_color_palette(['m', 'c', 'y', 'k'])

    fig, axes = plt.subplots(1, 2, figsize=(8, 3))

    dn1 = hierarchy.dendrogram(Z, ax=axes[0], above_threshold_color='y',

                               orientation='top')

    dn2 = hierarchy.dendrogram(Z, ax=axes[1],

                               above_threshold_color='#bcbddc',

                               orientation='right')

    hierarchy.set_link_color_palette(None)
    plt.show()


def dendrogram_plot(clusters):

    return;