import os
import redbaron
from code_analyzer.scriptReader import *

variables = []  # stores every found variable
vNames = []     # stores the name of every variable without repetitions

directory = "../ex1"


class variable:

    reassignment = []   # stores the line of every variable reassignment
    use = []   # stores the line of every used variable
    with_functions = []   # stores the line of every variable used within functions
    operators = []   # stores the line of every variable used with operators

    def __init__(self, name: str, line: str):
        self.name = name    # stores the name of the variable
        self.line = line    # stores the line of the first use in the variable

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


for root, dirs, files in os.walk(directory):
    for file in files:
        if file.endswith(".py"):
            filename = os.path.join(root, file)
            filename = filename.split("\\")[1]
            with open(os.path.join(root, file), "r") as f:
                red = redbaron.RedBaron(f.read())
                nodes = red.find_all("assignment")
                for node in nodes:
                    var = str(node).split(" = ")[0]
                    if '+' not in var and '-' not in var and '*' not in var and '/' not in var and '[' not in var:
                        if var not in vNames:
                            v = variable(var, "line " + str(node.absolute_bounding_box.top_left.line))
                            variables.append(v)
                            vNames.append(var)
                nodes = red.find_all("tuple")
                for node in nodes:
                    var = str(node).split(",")[0]
                    if var not in vNames:
                        v = variable(var, "line " + str(node.absolute_bounding_box.top_left.line))
                        variables.append(v)
                        vNames.append(var)
                nodes = red.find_all("for")
                for node in nodes:
                    if len(str(node.iterator).split(",")) > 1:
                        var = str(node.iterator).split(", ")
                        for v in var:
                            if v not in vNames:
                                vr = variable(v, "line " + str(node.absolute_bounding_box.top_left.line))
                                variables.append(vr)
                                vNames.append(var)
                    else:
                        if str(node.iterator) not in vNames:
                            v = variable(node.iterator, "line " + str(node.absolute_bounding_box.top_left.line))
                            variables.append(v)
                            vNames.append(str(node.iterator))

for vrr in variables:
    print(str(vrr.name) + " " + str(vrr.line))
