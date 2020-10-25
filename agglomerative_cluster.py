
import numpy as np
from sys import maxsize

class data_point:
    def __init__(self, vector_location, index, size=20):
        '''

        :param vector_location:type np.narray
        :param size:
        '''
        if len(vector_location) != size:
            self = None
        else:
            self.distance = maxsize
            self.center = vector_location
            self.number_of_points = 1
            self.index = index
    def get_top(self, depth):
        return [self]

def euc_distance(row):
    '''
    Calculates the euclidean distance from data_point_1 to data_point_2
    :param row:type Pandas.Series
    :return: the distance between points 1 and 2
    '''
    data_point_1 = row["cluster1"]
    data_point_2 = row["cluster2"]
    row["distance"] = np.linalg.norm(data_point_1.center-data_point_2.center)



class cluster:
    '''
    number datapoints
    cluster center x, y
    list datapoints
    '''
    def __init__(self, cluster1, cluster2, distance, index):
        if isinstance(cluster1, data_point):
            if isinstance(cluster2, data_point):
                self.data_points = [cluster1, cluster2]
            else:
                self.data_points = [cluster1] + cluster2.data_points
        else:
            if isinstance(cluster2, data_point):
                self.data_points = cluster1.data_points+ [cluster2]
            else:
                self.data_points = cluster1.data_points + cluster2.data_points
        self.index = index
        self.distance = distance
        self.number_of_points = len(self.data_points)
        self.center = self.new_center(cluster1, cluster2)
        self.left_cluster = cluster1
        self.right_cluster = cluster2


    def new_center(self, cluster1, cluster2):
        weighted_component = np.average([cluster1.center, cluster2.center], axis=0,
                                        weights = [cluster1.number_of_points, cluster2.number_of_points])
        return weighted_component
