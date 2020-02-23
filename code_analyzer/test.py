import os
import redbaron
from code_analyzer.scriptReader import *

# pene

"""
    lol
"""

# adeaded

# bazinga

file = "./test.py"
with open(file, "r") as f:
    red = redbaron.RedBaron(f.read())
    commentsOnCode(red)
