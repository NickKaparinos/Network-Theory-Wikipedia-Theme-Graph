# Network Theory Project
# Aristotle University of Thessaloniki
# Nick Kaparinos
# 2020

# The purpose of this script is to create and save a graph of wikipedia pages of a certain theme
# The theme of the graph is given in the string theme

import time

import networkx as nx
import wikipedia
#from gensim.summarization import keywords


def create_graph(theme, depth, breadth, rootBreadthMultiplier):
    # This function creates and builds the graph
    root = wikipedia.WikipediaPage(theme)
    G = nx.DiGraph()
    G.add_node(root.title)

    if (depth >= 1):
        # Calculate child nodes
        childNodesList = []

        counts = {}
        for i in root.links:
            searchString = i
            if(i.endswith(" music")):
                searchString = searchString.removesuffix(" music")

            counts[i] = root.content.lower().count(searchString.lower())
        counts = {k: v for k, v in sorted(counts.items(), key=lambda item: item[1], reverse=True)}

        #
        # key = keywords(root.content,split=True)
        # print("what")
        # keyl = keywords(root.content,split=True, lemmatize=True)
        fet = 5
        sfet = 5
        for k in counts:
            childNodesList.append(k)
            if len(childNodesList) > rootBreadthMultiplier * breadth:
                break

        for i in childNodesList:
            build_graph(G, depth, breadth, i, 1, root.title)
    return G


def build_graph(G, depth, breadth, node, current_depth, parentTitle):
    # Find page "node"
    try:
        node = wikipedia.WikipediaPage(node)
    except:  # wikipedia.DisambiguationError and wikipedia.exceptions.PageError
        return
    G.add_node(node.title)
    G.add_edge(parentTitle, node.title)
    if node.title == "Deep Purple":
        fet = 5
    fet2 = 6

    if (depth >= current_depth + 1):
        # Calculate child nodes
        childNodesList = []

        counts = {}
        for i in node.links:
            searchString = i
            if(i.endswith(" music")):
                 searchString = searchString.removesuffix(" music")
            counts[i] = node.content.lower().count(searchString.lower())
        counts = {k: v for k, v in sorted(counts.items(), key=lambda item: item[1], reverse=True)}
        for k in counts:
            childNodesList.append(k)
            if (len(childNodesList) >= breadth):
                break

        # Build the next level of the graph
        for i in childNodesList:
            if i not in G.nodes:
                build_graph(G, depth, breadth, i, current_depth + 1, node.title)
            else:
                G.add_edge(node.title, i)
    fet = 5


print('Network Theory')
theme = "Heavy metal music"
depth = 4
breadth = 7
rootBreadthMultiplier = 4

start = time.perf_counter()
G = create_graph(theme, depth, breadth, rootBreadthMultiplier)
end = time.perf_counter()

print(end - start)

debug = True
# plt.show()
#nx.write_gexf(G,"HeavyMetal476.gexf")
#nx.write_gml(G, "HeavyMetal477.gml")
