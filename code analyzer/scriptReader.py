from redbaron import RedBaron

file = open("code analyzer/test.py")
red = RedBaron(file)
print(red.help())
