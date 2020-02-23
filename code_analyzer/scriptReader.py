
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
        result.insert(counter, "    >   " + str(node).split("#")[1] + ": line " + str(node.absolute_bounding_box.top_left.line))
    return result

# returns an integer with the number of all the functions
def countFunctions(red):
    nodes = red.find_all("def")
    return len(nodes)

# returns an integer with the number of all the variables
def countVariables(red):


# returns an integer with the number of all the libraries
def countLibraries(red):
    nodes = red.find_all("import")
    counter =  len(nodes)
    nodes = red.find_all("fromimport")
    counter += len(nodes)
    return counter

# returns an integer with the total number of lines in the code
def countLines(red):