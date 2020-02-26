import os
import redbaron
from code_analyzer.scriptReader import *

variables = []

directory = "../ex1"


class variable:
    def __init__(self, name: str, vType: str, line: str):
        self.name = name
        self.vType = vType
        self.line = line


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
                        for v in variables:
                            if var not in v:
                                v = variable(var, "First use", "line " + str(node.absolute_bounding_box.top_left.line))
                                variables.append(v)
                nodes = red.find_all("tuple")
                for node in nodes:
                    var = str(node).split(",")[0]
                    if var not in variables:
                        v = variable(var, "First use", "line " + str(node.absolute_bounding_box.top_left.line))
                        variables.append(v)
                nodes = red.find_all("for")
                for node in nodes:
                    if len(str(node.iterator).split(",")) > 1:
                        var = str(node.iterator).split(", ")
                        for v in var:
                            if v not in variables:
                                vr = variable(v, "First use", "line " + str(node.absolute_bounding_box.top_left.line))
                                variables.append(vr)
                    else:
                        if str(node.iterator) not in variables:
                            v = variable(node.iterator, "First use",
                                         "line " + str(node.absolute_bounding_box.top_left.line))
                            variables.append(v)

for vrr in variables:
    print(vrr.name + " " + vrr.vType + " " + vrr.line)
