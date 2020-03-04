import os
import redbaron
import networkx as nx
import matplotlib.pyplot as plt


class variable:
    reassignment = []  # stores the line of every variable reassignment
    use = []  # stores the line of every used variable
    with_functions = []  # stores the line of every variable used within functions
    operators = []  # stores the line of every variable used with operators

    def __init__(self, name: str, line: int):
        self.name = name  # stores the name of the variable
        self.line = line  # stores the line of the first use in the variable
        self.reassignment = []
        self.use = []
        self.with_functions = []
        self.operators = []

    def add_reassignment(self, var: str):
        if var not in self.reassignment:
            self.reassignment.append(var)

    def add_use(self, var: str):
        if var not in self.use:
            self.use.append(var)

    def add_with_functions(self, var: str):
        if var not in self.with_functions:
            self.with_functions.append(var)

    def add_operators(self, var: str):
        if var not in self.operators:
            self.operators.append(var)


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


# returns a variable list with all the used variables
def usedVariables(red):
    vList = []  # stores every found variable
    vNames = []  # stores the name of every variable without repetitions
    nodes = red.find_all("assignment")
    for node in nodes:
        var = str(node.name)
        if '+' and '-' and '*' and '/' not in var:
            if var not in vNames:
                v = variable(var, int(node.absolute_bounding_box.top_left.line))
                vList.append(v)
                vNames.append(var)
    nodes = red.find_all("tuple")
    for node in nodes:
        var = str(node.name)
        if var not in vNames:
            v = variable(var, int(node.absolute_bounding_box.top_left.line))
            vList.append(v)
            vNames.append(var)
    nodes = red.find_all("for")
    for node in nodes:
        if len(str(node.iterator).split(",")) > 1:
            var = str(node.iterator).split(", ")
            for v in var:
                if v not in vNames:
                    vr = variable(v, int(node.absolute_bounding_box.top_left.line))
                    vList.append(vr)
                    vNames.append(var)
        else:
            if str(node.iterator) not in vNames:
                v = variable(node.iterator, int(node.absolute_bounding_box.top_left.line))
                vList.append(v)
                vNames.append(str(node.iterator))
    # we search for every variable reassignment
    nodes = red.find_all("assignment")
    for node in nodes:
        var = str(node.name)
        if '+' and '-' and '*' and '/' not in var:
            for v in vList:
                if v.name == var:
                    if int(v.line) != int(node.absolute_bounding_box.top_left.line):
                        v.add_reassignment(node.absolute_bounding_box.top_left.line)
                        break
    # we search for every used variable
    nodes = red.find_all("comparison")
    for node in nodes:
        var = str(node)
        if ' < ' in var:
            var = var.split(' < ')
        elif ' > ' in var:
            var = var.split(' > ')
        elif ' == ' in var:
            var = var.split(' == ')
        elif ' != ' in var:
            var = var.split(' != ')
        for v in var:
            for vb in vList:
                if str(v) == vb.name:
                    if int(vb.line) != int(node.absolute_bounding_box.top_left.line):
                        vb.add_use(node.absolute_bounding_box.top_left.line)
    nodes = red.find_all("binaryOperator")
    for node in nodes:
        var = str(node)
        if ' + ' in var:
            var = var.split(' + ')
        elif ' - ' in var:
            var = var.split(' - ')
        elif ' * ' in var:
            var = var.split(' * ')
        elif ' / ' in var:
            var = var.split(' / ')
        for v in var:
            if '[' in v:
                v = v.split('[')[0]
            if '(' in v:
                v = v.split('(')[0]
            for vb in vList:
                if str(v) == vb.name:
                    if int(vb.line) != int(node.absolute_bounding_box.top_left.line):
                        vb.add_use(node.absolute_bounding_box.top_left.line)
    nodes = red.find_all("getItem")
    for node in nodes:
        var = str(node).split('[')[1]
        var = var.split(']')[0]
        if '(' in var:
            var = var.split('(')[1]
            var = var.split(')')[0]
        for v in var:
            for vb in vList:
                if str(v) == vb.name:
                    if int(vb.line) != int(node.absolute_bounding_box.top_left.line):
                        vb.add_use(node.absolute_bounding_box.top_left.line)
    nodes = red.find_all("atomTrailers")
    for node in nodes:
        counter = 0
        for n in node:
            var = str(n)
            if '(' in var:
                var = var.split('(')[1]
                var = var.split(')')[0]
            if '[' in var:
                var = var.split('[')[1]
                var = var.split(']')[0]
            if ',' in var:
                var = var.split(', ')
                for vr in var:
                    for v in vList:
                        if str(v.name) == vr and counter != 0:
                            v.add_use(node.absolute_bounding_box.top_left.line)
            else:
                for v in vList:
                    if str(v.name) == var and counter != 0:
                        v.add_use(node.absolute_bounding_box.top_left.line)
            counter += 1
    nodes = red.find_all("assignment")
    for node in nodes:
        var = str(node)
        if '+' or '-' or '*' or '/' in var:
            for v in vList:
                if var.split("= ")[1] == v.name:
                    v.add_use(node.absolute_bounding_box.top_left.line)
                    break
    # we search for every variable used within functions
    variab = []
    nodes = red.find_all("callArgument")
    for node in nodes:
        var = str(node)
        if '"' not in var:
            vr = []
            if '+' in var:
                vr.extend(var.split(' + '))
            if '-' in var:
                vr.extend(var.split(' - '))
            if '*' in var:
                vr.extend(var.split(' * '))
            if '/' in var:
                vr.extend(var.split(' / '))
            if '.' in var:
                vr.extend(var.split('.'))
            if '[' in var:
                v1 = var.split('[')[0]
                vr.append(v1)
            else:
                vr.append(var)
            for vari in vr:
                for v in vList:
                    if str(v.name) == vari:
                        found = False
                        for vb in variab:
                            if vari == vb:
                                found = True
                                break
                        if not found:
                            variab.append(vari)
                        break
    nodes = red.find_all("atomTrailers")
    for node in nodes:
        string = ""
        counter = 0
        for n in node:
            var = str(n)
            if '(' not in var:
                if counter == 0:
                    string = var
                else:
                    string += "." + var
            else:
                var = var.split("(")[1]
                var = var.split(")")[0]
                vr = []
                if ',' in var:
                    vr.extend(var.split(', '))
                if '+' in var:
                    vr.extend(var.split(' + '))
                if '-' in var:
                    vr.extend(var.split(' - '))
                if '*' in var:
                    vr.extend(var.split(' * '))
                if '/' in var:
                    vr.extend(var.split(' / '))
                if '.' in var:
                    vr.extend(var.split('.'))
                if '[' in var:
                    v1 = var.split('[')[0]
                    vr.append(v1)
                else:
                    vr.append(var)
                for vari in vr:
                    for v in vList:
                        if str(v.name) == vari:
                            found = False
                            for function in v.with_functions:
                                if string == str(function).split(':')[0]:
                                    function += ", " + str(node.absolute_bounding_box.top_left.line)
                                    found = True
                                    break
                            if not found:
                                v.add_with_functions(
                                    string + "(): line " + str(node.absolute_bounding_box.top_left.line))
                            break
            counter += 1
    # we search for every variable used with operators
    nodes = red.find_all("atomTrailers")
    for node in nodes:
        found = False
        for n in node:
            if found:
                if '[' not in str(n):
                    v.add_operators("." + str(n) + ": line " + str(node.absolute_bounding_box.top_left.line))
                    break
            for v in vList:
                if str(n) == v.name:
                    found = True
                    break
    return vList


# returns a string list with all the used functions
def usedFunctions(red):
    usedFunctions = [] # here we will store all the arrays for the result
    # we search for all the imported functions
    fromFunctions = []
    libraries = []
    lib = importedLibraries(red)
    for library in lib:
        library = library.split('   >   ')[1]
        library = library.split(':')[0]
        library = library.split(" ")[1]
        libraries.append(library)
    nodes = red.find_all("atomTrailers")
    for node in nodes:
        string = ""
        library = ""
        found = False
        for n in node:
            var = str(n)
            if '(' not in var:
                if not found:
                    for lib in libraries:
                        if var == lib:
                            found = True
                            library = var
                            break
                else:
                    string += "." + var
        if found:
            if not fromFunctions:
                fromFunctions.append([library, string + "():  line " + str(node.absolute_bounding_box.top_left.line)])
            else:
                found = False
                for lb in fromFunctions:
                    if lb[0] == library:
                        found = True
                        counter = 0
                        for fn in lb:
                            if counter != 0:
                                if fn.split('():')[0] == string:
                                    lb[counter] = lb[counter] + ", " + str(node.absolute_bounding_box.top_left.line)
                                    break
                            counter += 1
                        break
                if not found:
                    fromFunctions.append(
                        [library, string + "():  line " + str(node.absolute_bounding_box.top_left.line)])
    # we search for the generic functions
    generics = ["abs", "all", "any", "ascii", "bin", "bool", "bytearray", "bytes", "callable", "chr", "classmethod",
                "compile", "complex", "delattr", "dict", "dir", "divmod", "enumerate", "eval", "exec", "filter",
                "float", "format", "frozenset", "getattr", "globals", "hasattr", "hash", "help", "hex", "id", "input",
                "int", "isinstance", "issubclass", "iter", "len", "list", "locals", "map", "max", "memoryview", "min",
                "next", "object", "oct", "open", "ord", "pow", "print", "property", "range", "repr", "reversed",
                "round", "set", "setattr", "slice", "sorted", "@staticmethod", "str", "sum", "super", "tuple", "type",
                "vars", "zip", "capitalize", "casefold", "center", "count", "encode", "endswith", "expandtabs", "find",
                "format", "format_map", "index", "isalnum", "isalpha", "isdecimal", "isdigit", "isidentifier",
                "islower", "isnumeric", "isprintable", "isspace", "istitle", "isupper", "join", "ljust", "lower",
                "lstrip", "maketrans", "partition", "replace", "rfind", "rindex", "rjust", "rpartition", "rsplit",
                "rstrip", "split", "splitlines", "startswith", "strip", "swapcase", "title", "translate", "upper",
                "zfill", "append", "clear", "copy", "count", "extend", "index", "insert", "pop", "remove", "reverse",
                "sort", "clear", "copy", "fromkeys", "get", "items", "keys", "pop", "popitem", "setdefault", "update",
                "values", "add", "clear", "copy", "difference", "difference_update", "discard", "intersection",
                "intersection_update", "isdisjoint", "issubset", "issuperset", "pop", "remove", "symmetric_difference",
                "symmetric_difference_update", "union", "update"]
    genericFunctions = []
    nodes = red.find_all("atomTrailers")
    for node in nodes:
        for n in node:
            var = str(n)
            if '(' not in var:
                if var in generics:
                    if not genericFunctions:
                        genericFunctions.append(var + "(): line " + str(node.absolute_bounding_box.top_left.line))
                    else:
                        counter = 0
                        found = False
                        for fun in genericFunctions:
                            if var == fun.split('():')[0]:
                                genericFunctions[counter] = genericFunctions[counter] + ", " + str(node.absolute_bounding_box.top_left.line)
                                found = True
                                break
                            counter += 1
                        if not found:
                            genericFunctions.append(var + "(): line " + str(node.absolute_bounding_box.top_left.line))
    # we search for all the used functions with variables
    withVariable = []
    vNames = []  # stores the name of every variable without repetitions
    nodes = red.find_all("assignment")
    for node in nodes:
        var = str(node.name)
        if '+' and '-' and '*' and '/' not in var:
            if var not in vNames:
                vNames.append(var)
    nodes = red.find_all("tuple")
    for node in nodes:
        var = str(node.name)
        if var not in vNames:
            vNames.append(var)
    nodes = red.find_all("for")
    for node in nodes:
        if len(str(node.iterator).split(",")) > 1:
            var = str(node.iterator).split(", ")
            for v in var:
                if v not in vNames:
                    vNames.append(v)
        else:
            if str(node.iterator) not in vNames:
                vNames.append(str(node.iterator))
    nodes = red.find_all("atomTrailers")
    for node in nodes:
        string = str(node)
        n = str(node).split(".")
        for nd in n:
            var = str(nd)
            if '(' not in var:
                for v in vNames:
                    if str(v) == var:
                        if not withVariable:
                            withVariable.append([var, string + ": line " + str(node.absolute_bounding_box.top_left.line)])
                        else:
                            counter = 0
                            foundVar = False
                            foundFun = False
                            for vr in withVariable:
                                if vr[0] == var:
                                    foundVar = True
                                    for ln in vr:
                                        if counter != 0:
                                            if ln == string.split(':')[0]:
                                                vr[counter] = vr[counter] + str(node.absolute_bounding_box.top_left.line)
                                                foundFun = True
                                                break
                                        counter += 1
                                    break
                            if not foundVar:
                                if '(' in string:
                                    string = string.split("(")[0]
                                    withVariable.append([var, string + "(): line " + str(node.absolute_bounding_box.top_left.line)])
                                else:
                                    withVariable.append([var, string + ": line " + str(node.absolute_bounding_box.top_left.line)])
                            if not foundFun and foundVar:
                                for vr in withVariable:
                                    if vr[0] == var:
                                        if '(' in string:
                                            string = string.split("(")[0]
                                            vr.append(string + "(): line " + str(node.absolute_bounding_box.top_left.line))
                                        else:
                                            vr.append(string + ": line " + str(node.absolute_bounding_box.top_left.line))
                                        break
                        break
    # we recollect all the data we've found
    usedFunctions.append(fromFunctions)
    usedFunctions.append(genericFunctions)
    usedFunctions.append(withVariable)
    return usedFunctions


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
