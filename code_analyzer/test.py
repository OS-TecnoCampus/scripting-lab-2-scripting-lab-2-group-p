import os
import redbaron
from code_analyzer.scriptReader import *

variables = []

directory = "../ex1"
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
                        if var not in variables:
                            variables.append(var)
                nodes = red.find_all("tuple")
                for node in nodes:
                    var = str(node).split(",")[0]
                    if var not in variables:
                        variables.append(var)
                nodes = red.find_all("for")
                for node in nodes:
                    if len(str(node.iterator).split(",")) > 1:
                        var = str(node.iterator).split(", ")
                        for v in var:
                            if v not in variables:
                                variables.append(v)
                    else:
                        if str(node.iterator) not in variables:
                            variables.append(node.iterator)