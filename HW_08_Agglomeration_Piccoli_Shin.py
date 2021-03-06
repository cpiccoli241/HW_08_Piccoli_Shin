from argparse import ArgumentParser
from agglomerative_cluster import data_point, euc_distance, cluster
import pandas as pd
from scipy.spatial.distance import squareform
from scipy.spatial.distance import pdist
import dendro_gram as dg
from sklearn.cluster import KMeans
import numpy as np

def cross_correlation(dataf):
    """
    Takes dataf and calculates the cross correlation coefficient
    removes the column ID, from the dataframe
    :type dataf: pandas.Dataframe
    :return cross_correlation: pands.Dataframe
    """


    # calculate correlation
    correlation = remove_id(dataf).corr(method='pearson')
    return correlation


def remove_id(dataf, ID ='ID'):
    '''
    renmove the column ID from the dataframe
    :param dataf:type pandas.dataframe
    :param ID:the key value to remove
    :return: dataframe without the column id
    '''
    # get a list of the dataframe columns
    keys = dataf.columns.values.tolist()
    # remove the ID for correlation
    keys.remove(ID)
    return dataf[keys]


def get_strongest_correlated(dataf, column):
    """
    Gets the best correlation of dataf at specific column
    :param dataf:
    :param column:
    :return: best_correlation, attribute_name
    """
    best_correlation = 0
    best_index = 0
    # array of all the dataframes column names
    columns = dataf.columns.values

    index = 0
    # iterate through the row
    for atr in dataf[column]:
        # pick the highest correlation that isn't the same attribute
        if atr > best_correlation and columns[index] != column:
            best_correlation = atr
            best_index = index
        index += 1
    # return the best correlation and the column name
    return best_correlation, columns[best_index]


def find_least_correlated(corrs_dict):
    '''
    finds the worst correlation from the dict
    :param corrs_dict:
    :return: worst correlation
    '''
    worst_correlation = 1
    worst_atr = ''
    for key in corrs_dict:
        if worst_correlation > corrs_dict[key][0]:
            worst_correlation = corrs_dict[key][0]
            worst_atr = key

    return worst_correlation, worst_atr

def find_best_correlated(corrs_dict):
    '''
    Finds the best correlation from the dict
    :param corrs_dict:
    :return: best correlation
    '''
    best_correlation = 0
    best_atr = ''
    for key in corrs_dict:
        if best_correlation < corrs_dict[key][0]:
            best_correlation = corrs_dict[key][0]
            best_atr = key

    return corrs_dict[best_atr], best_atr

def question_2(dataf):
    '''
    Gives the necessary information to complete section 2 of report
    :param dataf:
    :return:
    '''
    keys = dataf.keys()
    correlations = {}
    for key in keys:
        corr, atr = get_strongest_correlated(dataf, key)
        correlations.update({key : [corr, atr]})

    best_atr, best_cor = find_best_correlated(correlations)
    print(best_atr, best_cor)

    # this is explicitly asked
    print("Fish: ", correlations['Fish'])
    print("Meat: ", correlations['Meat'])
    print("Beans: ", correlations['Beans'])

    # if we compare which one has the worst best correlation
    # that is similiar to finding the least correlated overall
    worst_correlation, worst_atr = find_least_correlated(correlations)
    print(worst_atr, worst_correlation)

    # remove the worst to find the second worst
    correlations.pop(worst_atr)

    # find the second worst the same as the first
    second_worst_correlation, second_worst_atr = find_least_correlated(correlations)
    print(second_worst_atr, second_worst_correlation)
    # and the final answer is to the last part of 2 is no
    '''
    See this article
    https://terrytao.wordpress.com/2014/06/05/when-is-correlation-transitive/
    In the Euclidean plane {{\bf R}^2}: {u} and {v} have a positive correlation of {\frac{1}{\sqrt{2}}}, as does {v}
    and {w}, but {u} and {w} are not correlated with each other. Or: for a typical undergraduate course, it is generally 
    true that good exam scores are correlated with a deep understanding of the course material, 
    and memorising from flash cards are correlated with good exam scores, but this does not imply 
    that memorising flash cards is correlated with deep understanding of the course material.
    '''

def agglomerative_clustering(dataf, number_of_clusters = 1):
    '''
    This function does the clustering algorithm. And stores the clusters into a tree for ease of use
    First we iterate through the dataframe and make each point into its own cluster
    then keep clustering ...
    :param dataf: The dataframe that has the data
    :return: agglomeratively clustered data
    '''

    cluster_centers = pd.DataFrame(dataf)

    # This loop takes in all 850 points and makes 850 datapoints
    temp = []
    for index in range(len(dataf)):
        vector = dataf.iloc[index].to_numpy()
        point = data_point(vector, index)
        temp.append({"cluster" : point})
    datapoints = pd.DataFrame(temp)

    # Clustering starts
    cluster_indexs = len(dataf)
    linkage_matrix = []
    while len(datapoints) != number_of_clusters:
        distances = compute_distance_matrix(cluster_centers)
        new_cluster, cluster1_id, cluster2_id = clustering(distances, datapoints, cluster_indexs)
        cluster_indexs+=1

        # remove the old clusters from the dataframe
        datapoints.drop(cluster1_id, axis=0, inplace=True)
        datapoints.drop(cluster2_id, axis=0, inplace=True)

        # add the new cluster to the dataframe
        datapoints = datapoints.append({'cluster': new_cluster}, ignore_index=True)

        # update all of the cluster centers
        cluster_centers.drop(cluster1_id, axis=0, inplace=True)
        cluster_centers.drop(cluster2_id, axis=0, inplace=True)

        cluster_centers = cluster_centers.append(pd.Series(new_cluster.center, dataf.columns), ignore_index=True)

        # Creating a linkage matrix for future use when creating dendrogram
        # we create it here since order matters
        linkage_matrix.append([new_cluster.left_cluster.index, new_cluster.right_cluster.index,
                              new_cluster.distance, new_cluster.number_of_points])

    return new_cluster, linkage_matrix, datapoints

def compute_distance_matrix(dataf):
    '''
    whole matrix of distances, gets all the distances between every point (Cluster)
    :param dataf: dataframe
    :return:
    '''
    matrix = pd.DataFrame(
        squareform(pdist(dataf)),
        columns=dataf.index,
        index=dataf.index)
    return matrix

def compute_distances(data_sets):
    '''
    computes all the distances between points
    :param data_sets:
    :return:
    '''
    distances = pd.DataFrame(data = {"cluster1" : data_sets, "cluster2" : data_sets}, columns=["cluster1", "cluster2", "distance"])
    data_copy = list(data_sets)

    for data_1 in data_sets:
        data_copy.remove(data_1)
        for data_2 in data_copy:
            distances = distances.append({"cluster1":data_1, "cluster2":data_2, "distance":euc_distance(data_1, data_2)}, ignore_index=True)

    return distances

# DEPRECATED
# def compute_distance(datasets, cluster, distances):
#     '''
#     computes the distance between one cluster, and the other datasets
#     :param datasets:
#     :param cluster:
#     :param distances:
#     :return:
#     '''
#     for data in datasets:
#         distances.append([cluster, data, euc_distance(cluster, data)])


def min_distance(dataf):
    '''
    Gets the min distance of the pairwise matrix
    :param dataf:
    :return: row of cluster2 distance
    '''
    min_distances = pd.DataFrame({"cluster2" :dataf[dataf.gt(0)].idxmin(0), "distances":dataf[dataf.gt(0)].min(0)})
    # returns all the rows with the min distances
    min_distances =  min_distances[min_distances['distances'] == min_distances['distances'].min()]

    # picks the first on in the list arbitarily
    pairs = min_distances[min_distances['cluster2'] == min_distances.index[0]]

    # this is a dataframe of size 1
    return pairs.index[0], pairs['cluster2'].iloc[0], pairs['distances'].iloc[0]


def clustering(distances, data_sets, index):
    '''
    Combines clusters and returns the old cluster's ID for future use
    :param distances: distance matrix
    :param data_sets: data
    :param index: order in which the cluster was created
    :return:
    '''

    # Gets the minimum distance between clusters
    cluster1_id, cluster2_id, distance = min_distance(distances)

    # Gets the clusters associated with minimum distance
    cluster1 = data_sets.loc[cluster1_id].cluster
    cluster2 = data_sets.loc[cluster2_id].cluster

    # merges the clusters together
    new_cluster = cluster(cluster1, cluster2, distance, index)

    #compute_distance(data_sets, new_cluster, distances)

    return new_cluster, cluster1_id, cluster2_id

def kmeans(dataf):
    '''
    Calculates the centers and counts for n = 6 clusters using KMeans
    :param dataf:
    :return:
    '''
    # Turn data into matrix
    mat = dataf.values
    # Do KMeans for 6 clusters
    km = KMeans(n_clusters=6)
    km.fit(mat)
    # Labels is used to count the number of items per cluster
    labels = km.labels_

    # This Loop is used to count
    zeroCount = 0
    oneCount = 0
    twoCount = 0
    threeCount = 0
    fourCount = 0
    fiveCount = 0
    for label in labels:
        if label == 0:
            zeroCount += 1
        if label == 1:
            oneCount += 1
        if label == 2:
            twoCount += 1
        if label == 3:
            threeCount += 1
        if label == 4:
            fourCount += 1
        if label == 5:
            fiveCount += 1

    # Print count and the centers
    print(zeroCount, oneCount, twoCount, threeCount, fourCount, fiveCount)
    print(np.array_str(km.cluster_centers_, precision=2))


def main():
    parser = ArgumentParser()
    # error if they as for help
    parser.add_argument('FILE_IN_NAME', help='Enter the file name you would like to use. Include any directories',)

    # get the filename argument
    FILE_IN_NAME = "HW_PCA_SHOPPING_CART_v896.csv"

    # read in the csv as a Dataframe
    shoping_cart_data = pd.read_csv(FILE_IN_NAME, index_col = False, error_bad_lines=False, skipinitialspace=True)
    pd.set_option('display.max_rows', None, 'display.max_columns', None)

    # cross correlation od pd
    cross = cross_correlation(shoping_cart_data)
    question_2(cross)

    #remove ids
    shoping_cart_data = remove_id(shoping_cart_data)


    #find the cluster
    cluster1, linkage_matrix, list_clusters = agglomerative_clustering(shoping_cart_data)


    # makes the dendrogram from the linkage list
    dg.dendrogram_plot(linkage_matrix, 20)

    # This is commented out since it is not important to the main program!
    # cluster1, linkage_matrix, six_clusters = get_6_clusters(shoping_cart_data)
    # for cluster in six_clusters['cluster']:
    #     print("ID: ", cluster.index)
    #     print("\tCenter: ", np.array_str(cluster.center, precision=2))
    #     print("\tSize: ", cluster.number_of_points)
    #
    # print(np.array_str(get_weighted_center(six_clusters), precision=2))

    # KMeans clustering its commented out since it is not important to main program
    # kmeans(shoping_cart_data)

def get_weighted_center(dataf):
    '''
    Returns the weighted center of the clusters in dataf
    dataf is a dataframe of clusters
    :param dataf:type pandas.Dataframe one row of clusters
    :return: np.array that is the wieghted center of the clusters
    '''
    centers = []
    sizes = []

    for cluster in dataf['cluster']:
        centers.append(cluster.center)
        sizes.append(cluster.number_of_points)

    weighted_component = np.average(centers, axis=0,
                                    weights=sizes)
    return weighted_component


def get_6_clusters(dataf):
    '''
    runs the clustring program and returns when there are only 6 clusters left.
    :param dataf: pandas.Dataframe the shopping data
    :return: last cluster made, linkage_matrix, list of 6 clusters
    '''
    return agglomerative_clustering(dataf, number_of_clusters=6)


if __name__ == '__main__':
    main()