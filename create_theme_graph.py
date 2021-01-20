# Network Theory Project
# Aristotle University of Thessaloniki
# Nick Kaparinos
# 2020

# The purpose of this script is to create and save a graph of wikipedia pages of a certain theme
# The theme of the graph is given in the string theme

import time

import networkx as nx
import wikipedia


def create_graph(theme, depth, breadth, rootBreadthMultiplier):
    # This function creates and builds the graph
    try:
        root = wikipedia.WikipediaPage(theme)
    except:  # wikipedia.DisambiguationError and wikipedia.exceptions.PageError
        print("Root node ERROR!")
        return

    G = nx.DiGraph()
    G.add_node(root.title)

    if (depth >= 1):
        # Calculate child nodes
        childNodesList = []

        # Count how many times every link appers in the page content and sort
        counts = {}
        for i in root.links:
            searchString = i
            if (i.endswith(" music")):  # sometimes a link appears in the page`s content
                searchString = searchString.removesuffix(" music")  # without the suffix " music"

            # if (i.endswith(" (American Band)")):
            #     searchString = searchString.removesuffix(" (American Band)")
            #
            # if (i.endswith(" (Band)")):
            #     searchString = searchString.removesuffix(" (Band)")

            counts[i] = root.content.lower().count(searchString.lower())
        counts = {k: v for k, v in sorted(counts.items(), key=lambda item: item[1], reverse=True)}

        # Links that appear most often are added in the child nodes list
        for k in counts:
            childNodesList.append(k)
            if len(childNodesList) > rootBreadthMultiplier * breadth:
                break

        # nodesDict keys are the nodes` title
        # nodesDict values are the depth that every node was added
        # it is used to prevent visiting a node again
        # depth is necessary because if a node was already visited but at a bigger depth, it should be revisited
        nodesDict = {}
        nodesDict[root.title] = 0
        for i in childNodesList:
            build_graph(G, depth, breadth, i, 1, root.title, nodesDict, theme)
    return G


def build_graph(G, depth, breadth, node, current_depth, parentTitle, nodesDict, theme):
    # Find page "node"
    try:
        node = wikipedia.WikipediaPage(node)
    except:  # wikipedia.DisambiguationError and wikipedia.exceptions.PageError
        return
    G.add_node(node.title)
    G.add_edge(parentTitle, node.title)
    nodesDict[node.title] = current_depth

    if (depth >= current_depth + 1):
        if (theme not in node.links):  # If the theme is not in links list, return
            return

        # Calculate child nodes
        childNodesList = []

        # Count how many times every link appers in the page content and sort
        counts = {}
        for i in node.links:
            searchString = i
            if (i.endswith(" music")):
                searchString = searchString.removesuffix(" music")
            counts[i] = node.content.lower().count(searchString.lower())
        counts = {k: v for k, v in sorted(counts.items(), key=lambda item: item[1], reverse=True)}

        # Links that appear most often are added in the child nodes list
        for k in counts:
            childNodesList.append(k)
            if (len(childNodesList) >= breadth):
                break

        # Build the next level of the graph
        for i in childNodesList:
            if i not in G.nodes:
                build_graph(G, depth, breadth - 1, i, current_depth + 1, node.title, nodesDict, theme)
            else:
                if nodesDict[i] > current_depth + 1:
                    # Revisit node
                    build_graph(G, depth, breadth - 1, i, current_depth + 1, node.title, nodesDict, theme)
                else:
                    G.add_edge(node.title, i)


if __name__ == "__main__":
    print('Network Theory Project:\nCreate Graph')
    theme = "Heavy metal music"
    print(f"Theme: {theme}")
    depth = 4
    print(depth)
    breadth = 10
    print(breadth)
    rootBreadthMultiplier = 5
    print(rootBreadthMultiplier)

    start = time.perf_counter()
    G = create_graph(theme, depth, breadth, rootBreadthMultiplier)
    end = time.perf_counter()

    print(f"Execution time = {end - start}")

    # plt.show()
    # nx.write_gexf(G,"HeavyMetal476.gexf")
    nx.write_gml(G, theme.replace(" ", "") + ".gml")
    # 4,7,6 411,887 kalo
