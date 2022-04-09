
from sys import platform

import sys
sys.path.insert(0, './src')
from dependencies import dependencies

import subprocess


def install(name, version=None):
    vstring = ""
    if version is not None:
        vstring = "==" + version
    if platform == "win32":
        subprocess.call(['pip', 'install', name + vstring])
    else:
        subprocess.call(['pip3', 'install', name + vstring])


for d in dependencies:
    print("bearly dancing setup installing " + d)
    if d is tuple:
        install(d[0], d[1])
    else:
        install(d)

print("good to go. bearly dancing.py in the src folder starts the game.")
