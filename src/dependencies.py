dependencies = ["pygame", "numpy", "cx-Freeze"]
dependencies.append("dill")

from sys import platform

if platform == "darwin":
    dependencies.append('pyobjc')
