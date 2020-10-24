
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

def euc_distance(data_point_1, data_point_2):
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
                self.center = cluster1
                self.data_points = [cluster1, cluster2]
            else:
                self.data_points = [cluster1].extend(cluster2.data_points)
        else:
            self.data_points = cluster1.data_points.extend(cluster2.data_points)

        self.left_cluster = cluster1
        self.right_cluster = cluster2


    def new_center(self, otherCluster):
        return;