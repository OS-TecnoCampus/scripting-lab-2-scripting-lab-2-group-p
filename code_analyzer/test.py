import os
import redbaron
from code_analyzer.scriptReader import *
import networkx as nx
import matplotlib.pyplot as plt

""""
directory = "../ex2"
G = nx.Graph()
totalLibraries = []  # here we store all the used libraries
functions = []  # here we store all the defined functions
scripts = []  # here we store lists with the libraries and the filename they are used in
filenames = []
for root, dirs, files in os.walk(directory):
    for file in files:
        if file.endswith(".py"):
            filename = os.path.join(root, file)
            filename = filename.split("\\")[1]
            if filename not in G.nodes:
                G.add_node(filename)
                if filename not in filenames:
                    filenames.append(filename)
            with open(os.path.join(root, file), "r") as f:
                red = redbaron.RedBaron(f.read())
                # we search for all the imports and from imports and store them
                nodes = red.find_all("import")
                fileLibraries = []
                for node in nodes:
                    fileLibraries.append(str(node).split("import ")[1])
                nodes = red.find_all("fromimport")
                for node in nodes:
                    if str(node).split("import ")[1] not in fileLibraries:
                        fileLibraries.append(str(node).split("import ")[1])
                for library in fileLibraries:
                    if library not in totalLibraries:
                        totalLibraries.append(library)
                libraries = [filename]
                libraries.extend(fileLibraries)
                scripts.append(libraries)
                # we search for all the defined functions and store them
                nodes = red.find_all("def")
                for node in nodes:
                    funct = str(node).split("def")[1].split(":")[0]
                    while funct in functions:
                        funct += "\u2028"
                    functions.append(funct)
                    G.add_node(funct)
                    G.add_edge(filename, funct)

for script in scripts:
    counter = 0
    for lib in script:
        if counter != 0:
            if lib + ".py" in filenames:
                G.add_edge(script[0], lib + ".py")
        counter += 1

nx.draw(G, pos=nx.spring_layout(G, k=1000), with_labels=True, node_size=2000, node_color='#00ecff', node_shape='s')
plt.savefig("../resources/graph.png")


# file = "./test.py"
file = "../ex1/task2.py"
counter = 0
with open(file, "r") as f:
    red = redbaron.RedBaron(f.read())
    print(countLibraries(red))
    counter += countLibraries(red)

with open(file, "r") as f2:
    red = redbaron.RedBaron(f2.read())
    """
