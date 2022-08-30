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


def shareTime(path):
    balances = []
    ginis = []
    nakamotos = []
    with open(path, "r") as f:
        reader = csv.reader(f, delimiter=",")
        for i, line in enumerate(reader):
            balances += line[1:-1]
            arr = np.asarray(line[1:-1], dtype=float)
            arr = arr[arr != 0]
            if len(arr) != 0:
                ginis.append(gini(arr))
                nakamotos.append(nakamoto(arr))
    # ginis = ginis[ginis != 0]
    return(ginis, nakamotos)


def frequencyHaus(path):
    members = genfromtxt(path, delimiter=',', dtype=str)
    votesCollection = collections.Counter(members[:, 1])
    votingFrequency = np.array(list(votesCollection.values()))
    return votingFrequency


def louvain(path, size):
    votesFlat = []
    proposalKeys = []
    voters = []
    votesByProposal = []
    proposals = 0
    with open(path, "r") as f:
        reader = csv.reader(f, delimiter=",")
        for i, line in enumerate(reader):
            proposals += 1
            votesFlat += line[1:-1]
            proposalKeys.append(line[0])
            votesByProposal.append(line[1:-1])
    print("done loop", path)
    votesCollection = collections.Counter(votesFlat)
    votingFrequency = np.array(list(votesCollection.values()))
    print("done freq:", path)
    arr = np.zeros(int(size-len(votesCollection.values())))
    votingFrequency = np.append(votingFrequency, arr)
    # for idx in range(int(size-len(votesCollection.values()))):
    #     votingFrequency = np.insert(votingFrequency, 0, 0)
    print("done freq2:", path)
    # voters = np.empty((0, 0))
    # for proposal in votesByProposal:
    #     for voter in proposal:
    #         voters = np.append(voters, voter)
    # voters = np.unique(voters)

    # print(voters.shape, votingFrequency.shape,
    #       np.array(list(votesCollection.keys())).shape)

    # # Create Adjacency Matrix
    # adjacencyList = np.zeros((len(voters), len(voters)))
    # for i, holder in enumerate(voters):
    #     for proposal in votesByProposal:
    #         if holder in proposal:
    #             for j in range(len(voters)):
    #                 if voters[j] in proposal:
    #                     adjacencyList[i][j] += 1

    # print(adjacencyList)
    # print(adjacencyList.shape)
    # # # draw the graph
    # fig3, ax3 = plt.subplots()
    # ax3.set_title("Louvain Communities")
    # G = nx.Graph()
    # for i in range(len(voters)):
    #     for j in range(len(voters)):
    #         if adjacencyList[i][j] != 0 and i != j:
    #             G.add_edge(i, j, weight=adjacencyList[i][j])

    # partition = community_louvain.best_partition(G, weight='weight')
    # # cmap = cm.get_cmap('viridis', max(partition.values()) + 1)
    # # shapes = 'so^>v<dph8'
    # # plt.figure(figsize=(12, 8))
    # # pos = nx.spring_layout(G)

    # # color the nodes according to their partition
    # # cmap = cm.get_cmap('viridis', max(partition.values()) + 1)
    # # nx.draw_networkx_edges(G, pos, alpha=0.5)
    # # for node, color in partition.items():
    # #     nx.draw_networkx_nodes(G, pos, [node], node_size=50,
    # #                            node_color=[cmap.colors[color]],
    # #                            node_shape=shapes[color])

    # # fig7, ax7 = plt.subplots()
    # # ax7.set_title("Louvain Communities")
    # # G = nx.Graph()
    # # for i in range(len(repHolders)):
    # #     for j in range(len(repHolders)):
    # #         if adjacencyList[i][j] != 0 and i != j:
    # #             G.add_edge(i, j, weight=adjacencyList[i][j])

    # cmap = cm.get_cmap('tab10', max(partition.values()) + 1)
    # plt.figure(figsize=(8, 8))
    # # draw the graph
    # # pos = nx.spring_layout(G)
    # pos = nx.kamada_kawai_layout(G)
    # # color the nodes according to their partition
    # cmap = cm.get_cmap('tab10', max(partition.values()) + 1)
    # colors = range(0, 450)
    # nx.draw_networkx_edges(G, pos,  alpha=0.05)
    # centrality = algo.degree_centrality(G)
    # for node, color in partition.items():
    #     if centrality[node] > 0.2:
    #         nx.draw_networkx_nodes(G, pos, [node], node_size=(centrality[node]*20)**2,
    #                                node_color=[cmap.colors[color]])
    # # # centrality analysis
    # # centrality = algo.degree_centrality(G)
    # # values = list(centrality.values())
    # # fig4, ax4 = plt.subplots()
    # # ax4.hist(np.sort(values), edgecolor='white',
    # #          linewidth=1.2, color="steelblue")
    # # ax4.set_ylabel("# of Members")
    # # ax4.set_xlabel("Degree Centrality")

    # # # centrality analysis
    # # fig5, ax5 = plt.subplots()
    # # ax5.hist(votingFrequency, edgecolor='white',
    # #          linewidth=1.2, color="steelblue")
    # # ax5.set_yscale("log")
    # # ax5.set_ylabel("Freq")
    # # ax5.set_xlabel("# Proposals Voted On")
    # print("HUHUU")
    # plt.show()
    return (votingFrequency, proposals)


# Curve
membersCurve = genfromtxt(
    '../onChain/ProtocolDAOs/Curve/members.csv', delimiter=',')
membersStrCurve = genfromtxt(
    '../onChain/ProtocolDAOs/Curve/members.csv', delimiter=',', dtype="str")
holdersCurve = membersCurve[membersCurve[:, 2] != 0, ]
lorenzCurve = lorenz(np.sort(holdersCurve[:, 2]))
(giniCurve, nakamotoCurve) = shareTime(
    '../onChain/ProtocolDAOs/Curve/shareTime2.csv')
print("curve:", giniCurve, nakamotoCurve)
(frequencyCurve, noCurveProposals) = louvain('../onChain/ProtocolDAOs/Curve/proposalVotes.csv',
                                             len(membersCurve[:, 1]))
proposalsCurveSnap = genfromtxt('../Snapshot/curve/proposals.csv',
                                delimiter="//")
(frequencyCurveSnap, no) = louvain('../Snapshot/curve/votes.csv',
                                   len(membersCurve[:, 1]))
noCurveProposalsSnap = len(proposalsCurveSnap[:, 0])

# Maker
membersMaker = genfromtxt(
    '../onChain/ProtocolDAOs/makerDao/members.csv', delimiter=',')
holdersMaker = membersMaker[membersMaker[:, 2] != 0, ]
lorenzMaker = lorenz(np.sort(holdersMaker[:, 2]))


# Uniswap
membersUni = genfromtxt(
    '../onChain/ProtocolDAOs/uniswap/members.csv', delimiter=',')
holdersUni = membersUni[membersUni[:, 1] != 0, ]
lorenzUni = lorenz(np.sort(holdersUni[:, 1]))
(giniUni, nakamotoUni) = shareTime(
    '../onChain/ProtocolDAOs/uniswap/shareTime.csv')
print("uni: ", giniUni, nakamotoUni, len(holdersUni[:, 0]))
(frequencyUni, noUniProposals) = louvain('../onChain/ProtocolDAOs/Uniswap/proposalVotes.csv',
                                         len(membersUni[:, 1]))
proposalsUniSnap = genfromtxt('../Snapshot/uniswap/proposals.csv',
                              delimiter="//")
(frequencyUniSnap, no) = louvain('../Snapshot/uniswap/votes.csv',
                                 len(membersUni[:, 1]))
noUniProposalsSnap = len(proposalsUniSnap[:, 0])
print("uni: ", frequencyUni)

# dxDao
membersDx = genfromtxt(
    '../onChain/DAOStack/dxDAO/reputationBalancesFormatted.csv', delimiter=';')
holdersDx = membersDx[membersDx[:, 0] != 0, ]
lorenzDx = lorenz(np.sort(holdersDx[1:, 0]))
shareTimeDx = genfromtxt(
    '../onChain/DAOStack/dxDAO/repTime.csv', delimiter=',')
(giniDx, nakamotoDx) = shareTime('../onChain/DAOStack/dxDAO/repTime.csv')
print("Dx:", giniDx, nakamotoDx)
(frequencyDx, noDxProposals) = louvain('../onChain/DAOStack/dxDAO/proposalVotes.csv',
                                       len(membersDx[:, 1]))

# Lao
membersLao = genfromtxt(
    '../onChain/DAOHaus/theLAO/members.csv', delimiter=',')
holdersLao = membersLao[membersLao[:, 2] != 0, ]
lorenzLao = lorenz(np.sort(holdersLao[:, 2]))
(giniLao, nakamotoLao) = shareTime(
    '../onChain/DAOHaus/theLAO/shareTime.csv')
print("Lao:", giniLao, nakamotoLao)
frequencyLao = frequencyHaus('../onChain/DAOHaus/theLAO/votes.csv')
noLaoProposals = 173


# Meta
membersMeta = genfromtxt(
    '../onChain/DAOHaus/MetaCartel/members.csv', delimiter='","', skip_header=1, dtype=float)
holdersMeta = membersMeta[membersMeta[:, 1] != 0, ]
lorenzMeta = lorenz(np.sort(holdersMeta[:, 1]))
(giniMeta, nakamotoMeta) = shareTime(
    '../onChain/DAOHaus/MetaCartel/shareTimeOld.csv')
print("Meta:", giniMeta, nakamotoMeta)
frequencyMeta = frequencyHaus(
    '../onChain/DAOHaus/MetaCartel/votes.csv')
proposalsMetaSnap = genfromtxt('../Snapshot/metaCartelVentures/proposals.csv',
                               delimiter="//")
(frequencyMetaSnap, no) = louvain('../Snapshot/metaCartelVentures/votes.csv',
                                  48)
noMetaProposals = 474
noMetaProposalsSnap = len(proposalsMetaSnap[:, 0])

# Moloch
membersMoloch = genfromtxt(
    '../onChain/DAOHaus/Moloch/membersWeb.csv', delimiter='","', skip_header=1, dtype=float)
holdersMoloch = membersMoloch[membersMoloch[:, 1] != 0, ]
lorenzMoloch = lorenz(np.sort(holdersMoloch[:, 1]))
(giniMoloch, nakamotoMoloch) = shareTime(
    '../onChain/DAOHaus/Moloch/shareTime.csv')
print("Moloch:", giniMoloch, nakamotoMoloch)
frequencyMoloch = frequencyHaus('../onChain/DAOHaus/Moloch/votes.csv')
noMolochProposals = 42

# ###################### gini CURVE ###########################
# # https://gist.github.com/CMCDragonkai/c79b9a0883e31b327c88bfadb8b06fc4
# # ensure your arr is sorted from lowest to highest values first!


with sns.color_palette("tab20", n_colors=10):
    with sns.axes_style("darkgrid"):
        fig1, ax1 = plt.subplots()
        ax1.plot(np.linspace(0.0, 1.0, lorenzDx.size),
                 lorenzDx, label='dxDao', linestyle='dotted')
        ax1.plot(np.linspace(0.0, 1.0, lorenzLao.size),
                 lorenzLao, label='Lao', linestyle='dashed')
        ax1.plot(np.linspace(0.0, 1.0, lorenzMeta.size),
                 lorenzMeta, label='Meta', linestyle='dashed')
        ax1.plot(np.linspace(0.0, 1.0, lorenzMoloch.size),
                 lorenzMoloch, linestyle='dashed', label='Moloch')
        ax1.plot(np.linspace(0.0, 1.0, lorenzUni.size),
                 lorenzUni, label='Uniswap', linestyle='dashdot')
        ax1.plot(np.linspace(0.0, 1.0, lorenzCurve.size),
                 lorenzCurve, label='Curve', linestyle='dashdot')
        ax1.plot(np.linspace(0.0, 1.0, lorenzMaker.size),
                 lorenzMaker, label='Maker', linestyle='dashdot')
        # plot the straight line perfect equality curve
        ax1.plot([0, 1], [0, 1], label='Perfect Equality', c="black")
        ax1.legend()
        ax1.set_ylabel("Fraction of Voting Rights")
        ax1.set_xlabel("Fraction of Voters")


with sns.color_palette("tab20", n_colors=10):
    with sns.axes_style("darkgrid"):
        fig2, ax2 = plt.subplots()
        ax2.plot(np.linspace(0.0, 1.0, len(giniDx)),
                 giniDx, label='dxDao', linestyle='dotted')
        ax2.plot(np.linspace(0.0, 1.0, len(giniLao)),
                 giniLao, label='Lao', linestyle='dashed')
        ax2.plot(np.linspace(0.0, 1.0, len(giniMeta)),
                 giniMeta, label='Meta', linestyle='dashed')
        ax2.plot(np.linspace(0.0, 1.0, len(giniMoloch)),
                 giniMoloch, linestyle='dashed', label='Moloch')
        ax2.plot(np.linspace(0.0, 1.0, len(giniCurve)),
                 giniCurve, label='Curve', linestyle='dashdot')
        ax2.plot(np.linspace(0.0, 1.0, len(giniUni)),
                 giniUni, label='Uni', linestyle='dashdot')
        # plot the straight line perfect equality curve
        ax2.legend()
        ax2.set_ylabel("Gini")
        ax2.set_xlabel("Time Interval (normalized)")

with sns.color_palette("tab20", n_colors=10):
    with sns.axes_style("darkgrid"):
        fig3, ax3 = plt.subplots()
        ax3.plot(np.linspace(0.0, 1.0, len(nakamotoDx)),
                 nakamotoDx, label='dxDao', linestyle='dotted')
        ax3.plot(np.linspace(0.0, 1.0, len(nakamotoLao)),
                 nakamotoLao, label='Lao', linestyle='dashed')
        ax3.plot(np.linspace(0.0, 1.0, len(nakamotoMeta)),
                 nakamotoMeta, label='Meta', linestyle='dashed')
        ax3.plot(np.linspace(0.0, 1.0, len(nakamotoLao)),
                 nakamotoLao, linestyle='dashed', label='Moloch')
        ax3.plot(np.linspace(0.0, 1.0, len(nakamotoCurve)),
                 nakamotoCurve, label='Curve', linestyle='dashdot')
        ax3.plot(np.linspace(0.0, 1.0, len(nakamotoUni)),
                 nakamotoUni, label='Uni', linestyle='dashdot')
        # plot the straight line perfect equality curve
        ax3.legend()
        ax3.set_ylabel("Nakamoto Coefficient")
        ax3.set_xlabel("Time Interval (normalized)")

# with sns.color_palette("tab20", n_colors=10):
#     with sns.axes_style("darkgrid"):
#         fig4, ((ax1, ax2, ax3, ax4), (ax5, ax6, ax7, ax8)) = plt.subplots(2, 4)
#         fig4.suptitle('Sharing x per column, y per row')
#         ax1.pie(np.sort(holdersCurve[:, 2]),  radius=3, center=(4, 4),
#                 wedgeprops={"linewidth": 1, "edgecolor": "white"}, frame=True)
#         ax2.pie(np.sort(holdersDx[1:, 0]),  radius=3, center=(4, 4),
#                 wedgeprops={"linewidth": 1, "edgecolor": "white"}, frame=True)
#         ax3.pie(np.sort(holdersLao[:, 2]),  radius=3, center=(4, 4),
#                 wedgeprops={"linewidth": 1, "edgecolor": "white"}, frame=True)
#         ax4.pie(np.sort(holdersMaker[:, 2]),  radius=3, center=(4, 4),
#                 wedgeprops={"linewidth": 1, "edgecolor": "white"}, frame=True)
#         ax5.pie(np.sort(holdersMeta[:, 1]),  radius=3, center=(4, 4),
#                 wedgeprops={"linewidth": 1, "edgecolor": "white"}, frame=True)
#         ax6.pie(np.sort(holdersMoloch[:, 1]),  radius=3, center=(4, 4),
#                 wedgeprops={"linewidth": 1, "edgecolor": "white"}, frame=True)
#         ax7.pie(np.sort(holdersUni[:, 1]),  radius=3, center=(4, 4),
#                 wedgeprops={"linewidth": 1, "edgecolor": "white"}, frame=True)

with sns.axes_style("dark"):
    fig4, ((ax1, ax2, ax3, ax4), (ax5, ax6, ax7, ax8)) = plt.subplots(2, 4)
    fig4.delaxes(ax8)

    c1 = plt.get_cmap('Blues')(np.linspace(0.2, 0.7, len(holdersDx[1:, 0])))
    ax1.pie(np.sort(holdersDx[1:, 0]),  radius=3, center=(4, 4),
            wedgeprops={"linewidth": 1, "edgecolor": "white"}, frame=True, colors=c1)
    ax1.set_xticklabels([])
    ax1.tick_params(left=False, bottom=False)
    ax1.set_yticklabels([])
    ax1.set_title("dxDao")
    c2 = plt.get_cmap('Blues')(np.linspace(0.2, 0.7, 1000))
    ax2.pie(np.flip(np.flip(np.sort(holdersCurve[:, 2]))[:1000]),  radius=3, center=(4, 4),
            wedgeprops={"linewidth": 1, "edgecolor": "white"}, frame=True, colors=c2)
    ax2.set_xticklabels([])
    ax2.tick_params(left=False, bottom=False)
    ax2.set_yticklabels([])
    ax2.set_title("Curve")
    c3 = plt.get_cmap('Blues')(np.linspace(0.2, 0.7, len(holdersMaker[:, 2])))
    ax3.pie(np.flip(np.flip(np.sort(holdersMaker[:, 2]))[:1000]),  radius=3, center=(4, 4),
            wedgeprops={"linewidth": 1, "edgecolor": "white"}, frame=True, colors=c3)
    ax3.set_xticklabels([])
    ax3.tick_params(left=False, bottom=False)
    ax3.set_yticklabels([])
    ax3.set_title("Maker")
    c4 = plt.get_cmap('Blues')(np.linspace(0.2, 0.7, 1000))
    ax4.pie(np.flip(np.flip(np.sort(holdersUni[:, 1]))[:1000]),  radius=3, center=(4, 4),
            wedgeprops={"linewidth": 1, "edgecolor": "white"}, frame=True, colors=c4)
    ax4.set_xticklabels([])
    ax4.tick_params(left=False, bottom=False)
    ax4.set_yticklabels([])
    ax4.set_title("Uniswap")
    c5 = plt.get_cmap('Blues')(np.linspace(0.2, 0.7, len(holdersLao[:, 2])))
    ax5.pie(np.sort(holdersLao[:, 2]),  radius=3, center=(4, 4),
            wedgeprops={"linewidth": 1, "edgecolor": "white"}, frame=True, colors=c5)
    ax5.set_xticklabels([])
    ax5.tick_params(left=False, bottom=False)
    ax5.set_yticklabels([])
    ax5.set_title("Lao")
    c6 = plt.get_cmap('Blues')(np.linspace(0.2, 0.7, len(holdersMoloch[:, 1])))
    ax6.pie(np.sort(holdersMoloch[:, 1]),  radius=3, center=(4, 4),
            wedgeprops={"linewidth": 1, "edgecolor": "white"}, frame=True, colors=c6)
    ax6.set_xticklabels([])
    ax6.tick_params(left=False, bottom=False)
    ax6.set_yticklabels([])
    ax6.set_title("Moloch")
    c7 = plt.get_cmap('Blues')(np.linspace(0.2, 0.7, len(holdersMeta[:, 1])))
    ax7.pie(np.sort(holdersMeta[:, 1]),  radius=3, center=(4, 4),
            wedgeprops={"linewidth": 1, "edgecolor": "white"}, frame=True, colors=c7)
    ax7.set_xticklabels([])
    ax7.tick_params(left=False, bottom=False)
    ax7.set_yticklabels([])
    ax7.set_title("MetaCartel")
    fig4.tight_layout()

frequencyDx = frequencyDx/noDxProposals
frequencyCurve = frequencyCurve/noCurveProposals
frequencyUni = frequencyUni/noUniProposals
frequencyLao = frequencyLao/noLaoProposals
frequencyMeta = frequencyMeta/noMetaProposals
frequencyMoloch = frequencyMoloch/noMolochProposals

votes = [frequencyDx, frequencyCurve, frequencyUni,
         frequencyLao, frequencyMeta, frequencyMoloch]
weights = [np.zeros_like(frequencyDx) + 1. / len(frequencyDx),
           np.zeros_like(frequencyCurve) + 1. / len(frequencyCurve),
           np.zeros_like(frequencyUni) + 1. / len(frequencyUni),
           np.zeros_like(frequencyLao) + 1. / len(frequencyLao),
           np.zeros_like(frequencyMeta) + 1. / len(frequencyMeta),
           np.zeros_like(frequencyMoloch) + 1. / len(frequencyMoloch)]
with sns.color_palette():
    with sns.axes_style("darkgrid"):
        fig5, ax2 = plt.subplots()
        ax2.hist(votes, weights=weights, label=['dxDao', 'Curve',
                 "Uniswap", "Lao", "MetaCartel", "Moloch"], bins=10)
        # ax2.hist(frequencyLao, label='Lao')
        # ax2.hist(frequencyMeta, label='Meta')
        # ax2.hist(frequencyMoloch, linestyle='dashed')
        # ax2.hist(frequencyCurve, weights=np.zeros_like(frequencyCurve) +
        #          1. / len(frequencyCurve), label='Curve')
        # ax2.hist(frequencyUni, label='Uni')
        # plot the straight line perfect equality curve
        ax2.legend()
        ax2.set_ylabel("% of Members (log)")
        ax2.set_yscale("log")
        ax2.set_xlabel("% of Votes Participated In")
        ax2.yaxis.set_major_formatter(
            mpl.ticker.PercentFormatter(1, decimals=3))
        ax2.xaxis.set_major_formatter(
            mpl.ticker.PercentFormatter(1))
        ax2.legend(prop={'size': 10})

frequencyCurveSnap = frequencyCurveSnap/noCurveProposalsSnap
frequencyMetaSnap = frequencyMetaSnap/noMetaProposalsSnap
frequencyUniSnap = frequencyUniSnap/noUniProposalsSnap
votes = [frequencyCurve, frequencyCurveSnap, frequencyUni,
         frequencyUniSnap, frequencyMeta, frequencyMetaSnap]
weights = [np.zeros_like(frequencyCurve) + 1. / len(frequencyCurve),
           np.zeros_like(frequencyCurveSnap) + 1. / len(frequencyCurveSnap),
           np.zeros_like(frequencyUni) + 1. / len(frequencyUni),
           np.zeros_like(frequencyUniSnap) + 1. / len(frequencyUniSnap),
           np.zeros_like(frequencyMeta) + 1. / len(frequencyMeta),
           np.zeros_like(frequencyMetaSnap) + 1. / len(frequencyMetaSnap)]
with sns.color_palette("tab20"):
    with sns.axes_style("darkgrid"):
        fig6, ax2 = plt.subplots()
        ax2.hist(votes, weights=weights, label=['Curve', 'Curve Snap',
                 "Uniswap", "Uniswap Snap", "MetaCartel", "MetaCartel Snap"], bins=10)
        # ax2.hist(frequencyLao, label='Lao')
        # ax2.hist(frequencyMeta, label='Meta')
        # ax2.hist(frequencyMoloch, linestyle='dashed')
        # ax2.hist(frequencyCurve, weights=np.zeros_like(frequencyCurve) +
        #          1. / len(frequencyCurve), label='Curve')
        # ax2.hist(frequencyUni, label='Uni')
        # plot the straight line perfect equality curve
        ax2.legend()
        ax2.set_ylabel("% of Members (log)")
        ax2.set_yscale("log")
        ax2.set_xlabel("% of Votes Participated In")
        ax2.yaxis.set_major_formatter(
            mpl.ticker.PercentFormatter(1, decimals=3))
        ax2.xaxis.set_major_formatter(
            mpl.ticker.PercentFormatter(1))
        ax2.legend(prop={'size': 10})

plt.show()

# C 2, M 2, U 1
# balancesCurve = []
# with open('../onChain/ProtocolDAOs/Curve/shareTime2.csv', "r") as f:
#     reader = csv.reader(f, delimiter=",")
#     for i, line in enumerate(reader):
#         balancesCurve += line[1:-1]
#         arr = np.asarray(line[1:-1], dtype=float)
#         arr = arr[arr != 0]
#         print(gini(arr))
#         print(np.amax(arr))
#         nakamoto(arr)
