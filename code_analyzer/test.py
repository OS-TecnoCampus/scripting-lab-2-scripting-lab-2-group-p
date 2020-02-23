import os
import redbaron
from code_analyzer.scriptReader import *


def pene():
    print("pene")


def hola():
    print("hola")


def nose(y):
    x = 4 + y
    return x


file = "./test.py"
with open(file, "r") as f:
    red = redbaron.RedBaron(f.read())
    definedFunctions(red)
