
import numpy as np

class data_point:
    def __init__(self, vector_location, size=20):
        '''

        :param vector_location:type np.narray
        :param size:
        '''
        if len(vector_location) != size:
            self = None
        else:
            self.location = vector_location
            self.center = vector_location
            self.number_of_points = 1


def euc_distance(data_point_1, data_point_2):
    '''
    Calculates the euclidean distance from data_point_1 to data_point_2
    :param data_point_1:
    :param data_point_2:
    :return: the distance between points 1 and 2
    '''
    return np.linalg.norm(data_point_1.location-data_point_2.location)


class cluster:
    '''
    number datapoints
    cluster center x, y
    list datapoints
    '''
    def __init__(self, cluster1, cluster2):
        if isinstance(cluster1, data_point):
            if isinstance(cluster2, data_point):
                self.data_points = [cluster1, cluster2]
            else:
                self.data_points = [cluster1].extend(cluster2.data_points)
        else:
            self.data_points = cluster1.data_points.extend(cluster2.data_points)

        self.new_center(cluster1, cluster2)
        self.left_cluster = cluster1
        self.right_cluster = cluster2


    def new_center(self, cluster1, cluster2):
        weighted_component = np.average([cluster1.center, cluster2.center],
                                        weights = [cluster1.number_of_points, cluster2.number_of_points])
        return weighted_component