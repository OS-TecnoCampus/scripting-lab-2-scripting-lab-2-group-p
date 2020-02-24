import os
import redbaron
from code_analyzer.scriptReader import *

text = "lole"

num = "5"

text = "pene"

lol = 41

num = "39"

text = "porque no va esto coño"

text = "porfavor funciona"

caca = 9

file = "./test.py"
with open(file, "r") as f:
    red = redbaron.RedBaron(f.read())
    usedVariables(red)
