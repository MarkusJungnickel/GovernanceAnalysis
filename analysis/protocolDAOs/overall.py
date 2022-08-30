# participation histogram
#   with snapshot comparison: curve, ave, uniswap, metaCartel
# Louvain:
#   all
#   all snpashot


from lib2to3.pytree import NodePattern
from math import trunc
from netrc import NetrcParseError
from pickle import BINBYTES
import string
from turtle import color
import matplotlib.pyplot as plt
import matplotlib as mpl
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
import seaborn as sns
from enum import Enum
import pandas as pd


class Column(Enum):
    PROPID = 0
    SPACENAME = 1
    SPACEID = 2
    AUTHOR = 3
    STATE = 4
    FOR = 5
    AGAINST = 6
    TOTAL = 7
    CREATED = 8
    VOTES = 9
    MEMBERS = 10
    PROPOSALS = 11
    PARTICIPATION = 12


###################### READ CSVS ###########################

# Aave
proposalsAave = genfromtxt(
    '../../onChain/ProtocolDAOs/Aave/proposals.csv', delimiter=",")
proposalsAave = proposalsAave[:, 4:8]

# Curve
proposalsCurve = genfromtxt(
    '../../onChain/ProtocolDAOs/Curve/proposals.csv', delimiter=",")
proposalsCurve = proposalsCurve[:, 4:6]

# Uniswap
proposalsUniswap = genfromtxt(
    '../../onChain/ProtocolDAOs/Uniswap/proposals.csv', delimiter=",")
proposalsUniswap = proposalsUniswap[:, 4:8]

################### CLEAN & COMBINE DATA ####################


###################### CONTROVERCY ###########################
proposals = np.append(proposalsAave, proposalsUniswap, axis=0)
propOutcomes = np.empty((len(proposals[:, 1]), 5))
for idx, prop in enumerate(proposals):
    # Participation
    propOutcomes[idx][0] = prop[0] + prop[1]
    # share majority
    propOutcomes[idx][1] = 0
    # share result
    propOutcomes[idx][2] = 0
    # vote result
    propOutcomes[idx][3] = 0
    # vote majority
    propOutcomes[idx][4] = 0
    if prop[2] > prop[3]:
        propOutcomes[idx][1] = prop[2]/(prop[2]+prop[3])
        propOutcomes[idx][2] = 1
        if prop[0] <= prop[1]:
            propOutcomes[idx][3] = 1
            propOutcomes[idx][4] = prop[1]/(prop[1]+prop[0])
        else:
            propOutcomes[idx][4] = prop[0]/(prop[1]+prop[0])
    else:
        propOutcomes[idx][1] = prop[3]/(prop[2]+prop[3])
        propOutcomes[idx][2] = 0
        if prop[1] < prop[0]:
            propOutcomes[idx][3] = 1
            propOutcomes[idx][4] = prop[0]/(prop[0]+prop[1])
        else:
            propOutcomes[idx][4] = prop[1]/(prop[0]+prop[1])

print("Shares vs votes differ: ", np.count_nonzero(
    propOutcomes[:, 3])/len(propOutcomes[:, 3]))
propOutcomes = propOutcomes[propOutcomes[:, 1] != 0, :]
# Controvercy histrogram
# fig2, ax2 = plt.subplots()
# ax2.set_box_aspect(1)
# ax2.hist(propOutcomes[:, 1], edgecolor='white',
#          linewidth=1.2, color="tab:orange")
# ax2.set_yscale("log")
# ax2.set_ylabel("Frequency")
# ax2.set_xlabel("Size of Majority")
# Controvercy histrogram
fig2, ax2 = plt.subplots()
weights = [np.zeros_like(propOutcomes[:, 1]) + 1. / len(propOutcomes[:, 1])]
ax2.hist(propOutcomes[:, 1], edgecolor='white',
         linewidth=1.2, color="tab:orange", weights=weights)
ax2.set_yscale("log")
ax2.set_ylabel("% of Proposals(log)")
ax2.yaxis.set_major_formatter(
    mpl.ticker.PercentFormatter(1))
ax2.xaxis.set_major_formatter(
    mpl.ticker.PercentFormatter(1))
ax2.set_xlabel("Size of Majority")


# Controvercy jointplot hex
fig3, ax3 = plt.subplots()
ax3.set_box_aspect(1)
sns.set_theme(style="ticks")
s1 = sns.jointplot(x=propOutcomes[:, 0], y=propOutcomes[:, 1], kind="hex",
                   norm=mpl.colors.LogNorm(), marginal_kws=dict(bins=13), joint_kws=dict(gridsize=15), color="tab:orange")
s1.ax_joint.set_xlabel('Voters')
s1.ax_joint.set_ylabel('Majority')

sns.set_theme(style="ticks", palette="flare")
fig6, ax6 = plt.subplots()
ax6.set_box_aspect(1)
outcomes = np.column_stack((propOutcomes[:, 1], propOutcomes[:, 4]))
outcomes = pd.DataFrame(outcomes, columns=['Share Majority', 'Vote Majority'])
s3 = sns.lmplot(data=outcomes, x="Share Majority",
                y="Vote Majority")


print("Median Participation:", np.median(propOutcomes[:, 0]))
print("Mean", outcomes.mean())
print("# Proposals:", len(propOutcomes[:, 0]))
