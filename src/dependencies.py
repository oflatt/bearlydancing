dependencies = [("pygame", "2.1.2"),
                "numpy", "cx-Freeze", "typing",
                "mypy", "colormath", "dill"]

from sys import platform


if platform == "darwin":
    dependencies.append('pyobjc')
    dependencies.append('six')
    dependencies.append('appdirs')
    dependencies.append('AppKit')
