import os
import redbaron
from code_analyzer.scriptReader import *

text = "lole"

num = "5"

str(text)

int(num)

str(text)

print(text)

file = "./test.py"
with open(file, "r") as f:
    red = redbaron.RedBaron(f.read())
    usedFunctions(red)
