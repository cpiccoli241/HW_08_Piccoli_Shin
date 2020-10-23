from argparse import ArgumentParser
import pandas as pd


def cross_correlation(dataf, ID='ID'):
    """
    Takes dataf and calculates the cross correlation coefficient
    removes the column ID, from the dataframe
    :type dataf: pandas.Dataframe
    :return cross_correlation: pands.Dataframe
    """

    # get a list of the dataframe columns
    keys = dataf.columns.values.tolist()
    # remove the ID for correlation
    keys.remove(ID)
    # calculate correlation
    correlation = dataf[keys].corr(method='pearson')
    return correlation

def main():
    parser = ArgumentParser()
    # error if they as for help
    parser.add_argument('FILE_IN_NAME', help='Enter the file name you would like to use. Include any directories')

    # get the filename argument
    FILE_IN_NAME = parser.parse_args().FILE_IN_NAME

    # read in the csv as a Dataframe
    shoping_cart_data = pd.read_csv(FILE_IN_NAME, index_col = False, error_bad_lines=False)
    pd.set_option('display.max_rows', None, 'display.max_columns', None)

    cross = cross_correlation(shoping_cart_data)
    print(cross.head())

if __name__ == '__main__':
    main()