import os
import redbaron
import networkx as nx
import matplotlib.pyplot as plt


# returns a string list with all the imported libraries (including ones with the operation "from")
def importedLibraries(red):
    nodes = red.find_all("import")
    result = []
    counter = 0
    for node in nodes:
        result.insert(counter, "    >   " + str(node).split("import")[1] + ": line " + str(
            node.absolute_bounding_box.top_left.line))
        counter += 1
    nodes = red.find_all("fromimport")
    for node in nodes:
        result.insert(counter, "    >   " + str(node).split("import")[1] + ": line " + str(
            node.absolute_bounding_box.top_left.line))
        counter += 1
    return result


# returns a string list with all the defined functions
def definedFunctions(red):
    nodes = red.find_all("def")
    result = []
    counter = 0
    for node in nodes:
        result.insert(counter, "    >   " + str(node).split("def")[1].split(":")[0] + ": line " + str(
            node.absolute_bounding_box.top_left.line))
        counter += 1
    return result


# returns a string list with all the comments in the code
def commentsOnCode(red):
    nodes = red.find_all("comment")
    result = []
    counter = 0
    for node in nodes:
        result.insert(counter,
                      "    >   " + str(node).split("#")[1] + ": line " + str(node.absolute_bounding_box.top_left.line))
    return result


# returns a string list with all the used variables
def usedVariables(directory):
    return ""


# returns a string list with all the used functions
def usedFunctions(directory):
    return ""


# generates the graph of the structure of the directory
def graphGenerator(directory):
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

    # we generate the edges for the libraries
    for script in scripts:
        counter = 0
        for lib in script:
            if counter != 0:
                if lib + ".py" in filenames:
                    G.add_edge(script[0], lib + ".py")
            counter += 1

    nx.draw(G, pos=nx.spring_layout(G, k=1000), with_labels=True, node_size=2000, node_color='#00ecff', node_shape='s')
    plt.savefig("../resources/graph.png")


# returns an integer with the number of all the functions
def countFunctions(red):
    nodes = red.find_all("def")
    return len(nodes)


# returns an integer with the number of all the variables
def countVariables(directory):
    variables = []
    vCount = 0
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                with open(os.path.join(root, file), "r") as f:
                    red = redbaron.RedBaron(f.read())
                    nodes = red.find_all("assignment")
                    for node in nodes:
                        var = str(node).split(" = ")[0]
                        if '+' not in var and '-' not in var and '*' not in var and '/' not in var and '[' not in var:
                            if var not in variables:
                                variables.append(var)
                                vCount += 1
                    nodes = red.find_all("tuple")
                    for node in nodes:
                        var = str(node).split(",")[0]
                        if var not in variables:
                            variables.append(var)
                            vCount += 1
                    nodes = red.find_all("for")
                    for node in nodes:
                        if len(str(node.iterator).split(",")) > 1:
                            var = str(node.iterator).split(", ")
                            for v in var:
                                if v not in variables:
                                    variables.append(v)
                                    vCount += 1
                        else:
                            if str(node.iterator) not in variables:
                                variables.append(node.iterator)
                                vCount += 1
    return vCount


# returns an integer with the number of all the libraries
def countLibraries(directory):
    libraries = []
    filenames = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                filenames.append(str(file).split(".py")[0])
        for file in files:
            with open(os.path.join(root, file), "r") as f2:  # cuidado con el f2
                red = redbaron.RedBaron(f2.read())
                nodes = red.find_all("import")
                for node in nodes:
                    if str(node).split("import ")[1] not in filenames:
                        if str(node) not in libraries:
                            libraries.append(str(node))
                nodes = red.find_all("fromimport")
                for node in nodes:
                    if str(node).split("import ")[1] not in filenames:
                        if str(node) not in libraries:
                            libraries.append(str(node))
    return len(libraries)


# returns an integer with the total number of lines in the code
def countLines(directory):
    count = len(open(directory).readlines())
    count += 1  # the readLines() function does not take into account the final blank lines at the end of every script,
    # so we add them manually
    return count
