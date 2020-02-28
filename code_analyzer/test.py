import os
import redbaron
from code_analyzer.scriptReader import *

directory = "../ex1"
variables = []  # stores every found variable


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


for root, dirs, files in os.walk(directory):
    for file in files:
        if file.endswith(".py"):
            filename = os.path.join(root, file)
            filename = filename.split("\\")[1]
            vList = []  # stores every found variable
            vNames = []  # stores the name of every variable without repetitions
            with open(os.path.join(root, file), "r") as f:
                # we search for the first use of every variable
                red = redbaron.RedBaron(f.read())
                nodes = red.find_all("assignment")
                for node in nodes:
                    var = str(node.name)
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
                    for n in node:
                        for v in vList:
                            if str(node) == v.name:
                                v.add_use(node.absolute_bounding_box.top_left.line)
                variables.extend(vList)
"""
for v in variables:
    print(v.name)
    # print(v.line)
    # print(v.reassignment)
    print(v.use)
"""