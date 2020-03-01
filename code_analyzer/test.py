import os
import redbaron
from code_analyzer.scriptReader import *

directory = "../ex1"
fromFunctions = []
libraries = []

for root, dirs, files in os.walk(directory):
    for file in files:
        if file.endswith(".py"):
            filename = os.path.join(root, file)
            filename = filename.split("\\")[1]
            vList = []  # stores every found variable
            vNames = []  # stores the name of every variable without repetitions
            with open(os.path.join(root, file), "r") as f:
                #   we search for every library function
                red = redbaron.RedBaron(f.read())
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
                                fromFunctions.append([library, string + "():  line " + str(node.absolute_bounding_box.top_left.line)])

for libr in libraries:
    print(libr)
for fn in fromFunctions:
    for l in fn:
        print(str(l))


"""
variables = []  # stores every found variable

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
                        elif '-' in var:
                            vr.extend(var.split(' - '))
                        elif '*' in var:
                            vr.extend(var.split(' * '))
                        elif '/' in var:
                            vr.extend(var.split(' / '))
                        elif '.' in var:
                            vr.extend(var.split('.'))
                        elif '[' in var:
                            v1 = var.split('[')[0]
                            v2 = var.split('[')[1]
                            v2 = v2.split(']')[0]
                            vr.extend(v1)
                            vr.extend(v2)
                        else:
                            vr.extend(var)
                        for vari in vr:
                            for v in vList:
                                if str(v.name) == vari:
                                    variab.append(vari)
                                    break
                nodes = red.find_all("atomTrailers")
                for vri in variab:
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
                                if '+' in var:
                                    vr.extend(var.split(' + '))
                                elif '-' in var:
                                    vr.extend(var.split(' - '))
                                elif '*' in var:
                                    vr.extend(var.split(' * '))
                                elif '/' in var:
                                    vr.extend(var.split(' / '))
                                elif '.' in var:
                                    vr.extend(var.split('.'))
                                elif '[' in var:
                                    v1 = var.split('[')[0]
                                    v2 = var.split('[')[1]
                                    v2 = v2.split(']')[0]
                                    vr.extend(v1)
                                    vr.extend(v2)
                                else:
                                    vr.extend(var)
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
                                                v.add_with_functions(string + ": line " + str(node.absolute_bounding_box.top_left.line))
                                            break
                            counter += 1
                # we search for every variable used with operators
                nodes = red.find_all("atomTrailers")
                for node in nodes:
                    found = False
                    for n in node:
                        if found:
                            if '[' not in str(n):
                                v.add_operators(
                                    "." + str(n) + ": line " + str(node.absolute_bounding_box.top_left.line))
                                break
                        for v in vList:
                            if str(n) == v.name:
                                found = True
                                break
                variables.extend(vList)

for v in variables:
    print(str(v.name))
    print(str(v.with_functions))
"""