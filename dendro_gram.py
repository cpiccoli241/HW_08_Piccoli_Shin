import matplotlib.pyplot as plt
from scipy.cluster import hierarchy, vq
from agglomerative_cluster import cluster
from HW_08_Agglomeration_Piccoli_Shin import  remove_id
import pandas as pd

def test():
    shoping_cart_data = pd.read_csv('HW_PCA_SHOPPING_CART_v896.csv', index_col=False, error_bad_lines=False, skipinitialspace=True)
    pd.set_option('display.max_rows', None, 'display.max_columns', None)
    shoping_cart_data = remove_id(shoping_cart_data)

    Z = hierarchy.linkage(shoping_cart_data.to_numpy(), )
    dn = hierarchy.dendrogram(Z)
    plt.show()

    # there are certainly 5 clusters
    dn2 = hierarchy.dendrogram(Z, truncate_mode='lastp', p = 12)
    plt.show()

    kmeans = vq.kmeans(shoping_cart_data.to_numpy())
    hierarchy.dendrogram(kmeans, truncate_mode='lastp', p=12)
    plt.scatter(k)


def dendrogram_plot(linkage, depth):
    # there are certainly 5 clusters
    dn2 = hierarchy.dendrogram(linkage, truncate_mode='lastp', p=depth)
    plt.show()
    return;

if __name__ == '__main__':
    test()