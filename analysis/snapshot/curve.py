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

###################### READ CSVS ###########################
proposals = genfromtxt('../../Snapshot/curve/proposals.csv',
                       delimiter="//")
emptyColumn = np.zeros((len(proposals[:, 0]), 1))
proposals = np.append(proposals, emptyColumn, axis=1)
spaces = genfromtxt('../../Snapshot/overall/spacesOld.csv',
                    delimiter=',', dtype=str)
proposalsStr = genfromtxt(
    '../../Snapshot/curve/proposals.csv', delimiter="//", dtype=str)

################### CLEAN & COMBINE DATA ####################
assert(len(proposalsStr[:, 0]) == len(proposals[:, 0]))
for idx, propStr in enumerate(proposalsStr):
    space = spaces[spaces[:, 0] == propStr[2], :]
    if len(space) == 0:
        space = [[0, 0]]
    proposals[idx][-1] = int(space[0][1])
proposals = proposals[proposals[:, -1] >= 50, :]
proposals = proposals[~np.isnan(proposals[:, 5]), :]
emptyColumn = np.zeros((len(proposals[:, 0]), 1))
proposals = np.append(proposals, emptyColumn, axis=1)
for prop in proposals:
    if prop[-2] >= prop[-3]:
        prop[-1] = prop[-3]/prop[-2]
    else:
        prop[-1] = 0


###################### CONTROVERCY ###########################
propOutcomes = np.empty((len(proposals[:, 1]), 5))
for idx, prop in enumerate(proposals):
    propOutcomes[idx][0] = prop[-1]
    propOutcomes[idx][3] = prop[-2]
    propOutcomes[idx][4] = prop[-3]
    if prop[5] > prop[6]:
        propOutcomes[idx][1] = prop[5]/(prop[5]+prop[6])
        propOutcomes[idx][2] = 1
    elif prop[6] > prop[5]:
        propOutcomes[idx][1] = prop[6]/(prop[5]+prop[6])
        propOutcomes[idx][2] = 0
    else:
        propOutcomes[idx][1] = 0
        propOutcomes[idx][2] = 0
propOutcomes = propOutcomes[propOutcomes[:, 1] != 0, :]


# Controvercy histrogram
fig2, ax2 = plt.subplots()
ax2.hist(propOutcomes[:, 1], edgecolor='white',
         linewidth=1.2, color="steelblue")
ax2.set_yscale("log")
ax2.set_ylabel("Frequency")
ax2.set_xlabel("Size of Majority")


# Controvercy Majority x Quorum
sns.set_theme(style="ticks")
s1 = sns.jointplot(x=propOutcomes[:, 0], y=propOutcomes[:, 1], kind="hex",
                   norm=mpl.colors.LogNorm(), marginal_kws=dict(bins=13), joint_kws=dict(gridsize=20))
s1.ax_joint.set_xlabel('Quorum')
s1.ax_joint.set_ylabel('Majority')

# Controvercy Majority x Size
sns.set_theme(style="ticks")
s2 = sns.jointplot(x=propOutcomes[:, 4], y=propOutcomes[:, 1], kind="hex",
                   norm=mpl.colors.LogNorm(), marginal_kws=dict(bins=10))
s2.ax_joint.set_xlabel('Size')
s2.ax_joint.set_ylabel('# Voters')


print("Median Size:", np.median(propOutcomes[:, 3]))
print("Median Quorum:", np.median(propOutcomes[:, 0]))
print("Median Majority:", np.average(propOutcomes[:, 1]))

# plt.show()


###################### COMMUNITIES ###########################

# Prepare data
votesFlat = []
proposalKeys = []
voters = []
votesByProposal = []
with open('../../Snapshot/curve/votes.csv', "r") as f:
    reader = csv.reader(f, delimiter=",")
    for i, line in enumerate(reader):
        votesFlat += line[1:-1]
        proposalKeys.append(line[0])
        votesByProposal.append(line[1:-1])
votesCollection = collections.Counter(votesFlat)
votingFrequency = np.array(list(votesCollection.values()))
for idx in range(int(proposals[0][-2]-len(votesCollection.values()))):
    votingFrequency = np.insert(votingFrequency, 0, 0)
voters = np.empty((0, 0))
for proposal in votesByProposal:
    for voter in proposal:
        voters = np.append(voters, voter)
voters = np.unique(voters)

# print(voters.shape, votingFrequency.shape,
#       np.array(list(votesCollection.keys())).shape)

# Create Adjacency Matrix
adjacencyList = np.zeros((len(voters), len(voters)))
for i, holder in enumerate(voters):
    for proposal in votesByProposal:
        if holder in proposal:
            for j in range(len(voters)):
                if voters[j] in proposal:
                    adjacencyList[i][j] += 1


# draw the graph
fig3, ax3 = plt.subplots()
ax3.set_title("Louvain Communities")
G = nx.Graph()
for i in range(len(voters)):
    for j in range(len(voters)):
        if adjacencyList[i][j] != 0 and i != j:
            G.add_edge(i, j, weight=adjacencyList[i][j])

partition = community_louvain.best_partition(G, weight='weight')
cmap = cm.get_cmap('viridis', max(partition.values()) + 1)
shapes = 'so^>v<dph8'
plt.figure(figsize=(12, 8))
pos = nx.spring_layout(G)

# color the nodes according to their partition
cmap = cm.get_cmap('viridis', max(partition.values()) + 1)
nx.draw_networkx_edges(G, pos, alpha=0.5)
for node, color in partition.items():
    nx.draw_networkx_nodes(G, pos, [node], node_size=50,
                           node_color=[cmap.colors[color]],
                           node_shape=shapes[color])

# centrality analysis
centrality = algo.degree_centrality(G)
values = list(centrality.values())
fig4, ax4 = plt.subplots()
ax4.hist(np.sort(values), edgecolor='white', linewidth=1.2, color="steelblue")
ax4.set_ylabel("# of Members")
ax4.set_xlabel("Degree Centrality")

# centrality analysis
fig5, ax5 = plt.subplots()
ax5.hist(votingFrequency, edgecolor='white', linewidth=1.2, color="steelblue")
ax5.set_yscale("log")
ax5.set_ylabel("Freq")
ax5.set_xlabel("# Proposals Voted On")


plt.show()


##################### BACKUP ###########################

# map = np.empty((51, 101))
# for prop in propOutcomes:
#     participation = prop[0]
#     majority = prop[1]
#     map[int(majority/(1/50))][int(participation/(100000/100))] += 1
# print(map)
# map = np.log(map)

# Controvercy Scatter Plot
# fig1, ax1 = plt.subplots()
# ax1.scatter(propOutcomes[:, 0], propOutcomes[:, 1],
#             c=propOutcomes[:, 2], cmap='RdYlGn')
# ax1.set_ylim(0.5)
# ax1.set_xscale('log')
# ax1.set_ylabel("Size of Majority")
# ax1.set_xlabel("Participation")
