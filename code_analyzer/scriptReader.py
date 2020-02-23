
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


def definedFunctions(red):
    nodes = red.find_all("def")
    result = []
    counter = 0
    for node in nodes:
        result.insert(counter, "    >   " + str(node).split("def")[1].split(":")[0] + ": line " + str(
            node.absolute_bounding_box.top_left.line))
        counter += 1
    return result
