# Network Theory Project
# Aristotle University of Thessaloniki
# Nick Kaparinos
# 2020

# The purpose of this script is to analyse a graph given in a .gml file
import time

import matplotlib.pyplot as plt
import networkx as nx
import seaborn as sns

plt.ion()

if __name__ == "__main__":
    print("Network Theory Project:\nAnalyse Graph")
    start = time.perf_counter()

    G = nx.read_gml("Heavymetalmusic.gml")

    ### Anlyse Graph ###

    # Metrics
    if nx.is_weakly_connected(G):
        Gundirected = nx.to_undirected(G)
        center = nx.center(Gundirected)
        eccentricity = nx.eccentricity(Gundirected)
        diameter = nx.diameter(Gundirected)
        radius = nx.radius(Gundirected)

        # Average shortest path length
        averageShortestPath = nx.average_shortest_path_length(Gundirected)
    else:
        center = nx.center(G)
        eccentricity = nx.eccentricity(G)
        diameter = nx.diameter(G)
        radius = nx.radius(G)

        # Average shortest path length
        averageShortestPath = nx.average_shortest_path_length(G)

    # Density
    density = nx.density(G)

    # Transivity
    transivity = nx.transitivity(G)

    # Clustering coefficient
    clusteringCoeff = nx.average_clustering(G)

    # Centralities
    closenessCentrality = nx.closeness_centrality(G)
    betweensCentrality = nx.betweenness_centrality(G)
    katzCentrality = nx.katz_centrality_numpy(G)
    eigenCentrality = nx.eigenvector_centrality_numpy(G)

    # Page rank
    pageRank = nx.pagerank_scipy(G)

    # Hits Authorities
    hubs, authorities = nx.hits_scipy(G)

    # Results
    message = f"Analysis complete!\nExecution time = {time.perf_counter() - start:.2f} second(s).\nThe graph is "
    directed = "directed" if nx.is_directed(G) else "undirected"
    message += directed

    if nx.is_directed(G):
        if nx.is_strongly_connected(G):
            connected = " and strongly connected.\n"
        elif nx.is_weakly_connected(G):
            connected = " and weekly connected.\n"
        else:
            connected = " and disconnected\n"
    else:
        if nx.is_connected(G):
            connected = " and connected.\n"
        else:
            connected = " and disconnected\n"
    message += connected
    print(message)

    print(f"Number of nodes = {G.number_of_nodes()}\nNumber of edges = {G.number_of_edges()}")
    print(
        f"Center = {center}\ndiameter = {diameter}\nradius = {radius}\nAverage shortest path length = {averageShortestPath:.4f}\nDensity = {density:.4f}\nTransivity = {transivity:.4f}\nClustering coefficient = {clusteringCoeff:.4f}")

    # Degree plots
    degrees = [i[1] for i in list(G.degree)]
    inDegrees = [i[1] for i in list(G.in_degree)]
    outDegrees = [i[1] for i in list(G.out_degree)]

    sns.displot(degrees)
    plt.title("Node degree distribution")
    plt.xlabel("Node degree")

    sns.displot(inDegrees)
    plt.title("Node in degree distribution")
    plt.xlabel("Node in degree")

    sns.displot(outDegrees)
    plt.title("Node out degree distribution")
    plt.xlabel("Node out degree")

    sns.displot(eccentricity)
    plt.title("Eccentiricy distribution")
    plt.xlabel("Eccentricity")

    # Gather dictionaries in a list and sort them on values
    listOfDicts = [closenessCentrality, betweensCentrality, katzCentrality, eigenCentrality, pageRank, authorities,
                   hubs]
    dictNames = ["Closeness Centrality", "Betweens Centrality", "Katz Centrality", "Eigenvector Centrality",
                 "Page Rank",
                 "Authorities", "Hubs"]

    listOfDicts = [{k: v for k, v in sorted(i.items(), key=lambda item: item[1], reverse=True)} for i in listOfDicts]

    # Scatterplots of the 20 nodes with the highest values in each dictionary
    for i in range(len(listOfDicts)):
        dictionary = listOfDicts[i]
        name = dictNames[i]

        j = 0
        limit = 20
        dictToPlot = {}
        for k, v in dictionary.items():
            dictToPlot[k] = v
            j += 1
            if j == limit:
                break

        plt.figure(i + 5)
        sns.scatterplot(x=dictToPlot.values(), y=dictToPlot.keys())
        plt.title(name + f": {limit} nodes with the highest value")

plt.ioff()
plt.show()
