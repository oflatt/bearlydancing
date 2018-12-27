
from sys import platform

import sys
sys.path.insert(0, './src')
from dependencies import dependencies

import subprocess

def install(name):
    if platform == "win32":
        subprocess.call(['pip', 'install', name])
    else:
        subprocess.call(['pip3', 'install', name])


for d in dependencies:
    print("bearly dancing setup installing " + d)
    install(d)

print("good to go. bearly dancing.py in the src folder starts the game.")
