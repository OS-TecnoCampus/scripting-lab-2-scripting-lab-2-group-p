import os
import redbaron
from code_analyzer.scriptReader import *
import networkx as nx
import matplotlib.pyplot as plt

G = nx.DiGraph()




"""
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