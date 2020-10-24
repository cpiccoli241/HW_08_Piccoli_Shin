from argparse import ArgumentParser
from agglomerative_cluster import data_point, euc_distance, cluster
import pandas as pd
from sys import maxsize


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
    worst_correlation = 1
    worst_atr = ''
    for key in corrs_dict:
        if worst_correlation > corrs_dict[key][0]:
            worst_correlation = corrs_dict[key][0]
            worst_atr = key

    return worst_correlation, worst_atr


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

def agglomerative_clustering(dataf):
    '''
    This function does the clustering algorithm. And stores the clusters into a tree for ease of use
    First we iterate through the dataframe and make each point into its own cluster
    then keep clustering ...
    :param dataf: The dataframe that has the data
    :return: agglomeratively clustered data
    '''

    # This loop takes in all 850 points and makes 850 datapoints
    datapoints = []
    for index in range(len(dataf)):
        vector = dataf.iloc[index].to_numpy()
        point = data_point(vector)
        datapoints.append(point)

    # Clustering starts
    clusters = []
    while len(distances) > 1:
        distances = compute_distances(cluster, datapoints)
        cluster1, distances, datapoints = clustering(distances, datapoints)


def compute_distances(data_sets):
    '''
    computes all the distances between points
    :param data_sets:
    :return:
    '''
    distances = pd.DataFrame(data = None, index=["cluster1", "cluster2", "distance"])
    data_copy = list(data_sets)

    for data_1 in data_sets:
        data_copy.remove(data_1)
        for data_2 in data_copy:
            distances.append([data_1, data_2, euc_distance(data_1, data_2)])

    return distances


def compute_distance(datasets, cluster, distances):
    '''
    computes the distance between one cluster, and the other datasets
    :param datasets:
    :param cluster:
    :param distances:
    :return:
    '''
    for data in datasets:
        distances.append([cluster, data, euc_distance(cluster, data)])


def min_distance(dataf):
    return dataf.min(level = "distance")


def clustering(distances, data_sets):
    best_row = min_distance(distances)
    cluster1 = best_row["cluster1"]
    cluster2 = best_row["cluster2"]

    # drop all the rows with the clusters 1 or 2 in them
    distances = distances[distances["cluster1"] != cluster1]
    distances = distances[distances["cluster1"] != cluster2]
    distances = distances[distances["cluster2"] != cluster1]
    distances = distances[distances["cluster2"] != cluster2]
    new_cluster = cluster(cluster1, cluster2)

    compute_distance(data_sets, new_cluster, distances)
    data_sets.remove(cluster1)
    data_sets.remove(cluster2)

    return new_cluster, distances, data_sets


def main():
    parser = ArgumentParser()
    # error if they as for help
    parser.add_argument('FILE_IN_NAME', help='Enter the file name you would like to use. Include any directories',)

    # get the filename argument
    FILE_IN_NAME = parser.parse_args().FILE_IN_NAME

    # read in the csv as a Dataframe
    shoping_cart_data = pd.read_csv(FILE_IN_NAME, index_col = False, error_bad_lines=False, skipinitialspace=True)
    pd.set_option('display.max_rows', None, 'display.max_columns', None)

    # cross correlation od pd
    cross = cross_correlation(shoping_cart_data)
    question_2(cross)
    

if __name__ == '__main__':
    main()