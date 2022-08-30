from lib2to3.pytree import NodePattern
from math import trunc
from netrc import NetrcParseError
import string
import matplotlib.pyplot as plt
from numpy import genfromtxt
import numpy as np
from matplotlib import cm, pyplot as plt
from pygini import gini
import collections
import csv
import networkx as nx
import networkx.algorithms.community as nx_comm
import networkx.algorithms as algo
import community as community_louvain
import pandas as pd
import seaborn as sns
import matplotlib as mpl


def lorenz(arr):
    scaled_prefix_sum = arr.cumsum() / arr.sum()
    return np.insert(scaled_prefix_sum, 0, 0)


def nakamoto(arr):
    arr = np.sort(arr)
    arr = np.flip(arr)
    total = np.sum(arr)
    sum = 0
    for idx, element in enumerate(arr):
        sum += element
        if sum/total > 0.5:
            count = idx+1
            return count


# APple
appleShareholders = genfromtxt(
    './apple.csv', delimiter=';')
shares = appleShareholders[:, 6]
shares = shares[~np.isnan(shares)]
giniCo = gini(np.sort(shares))
print(nakamoto(shares))
print(giniCo)


# APple
appleShareholders = genfromtxt(
    './amzn.csv', delimiter=';')
shares = appleShareholders[:, 6]
shares = shares[~np.isnan(shares)]
giniCo = gini(np.sort(shares))
print(nakamoto(shares))
print(giniCo)


# APple
appleShareholders = genfromtxt(
    './msft.csv', delimiter=';')
shares = appleShareholders[:, 6]
shares = shares[~np.isnan(shares)]
giniCo = gini(np.sort(shares))
print(nakamoto(shares))
print(giniCo)
