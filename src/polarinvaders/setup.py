import sys
from cx_Freeze import setup, Executable

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

includefiles = []
build_exe_options = {"packages" : ["pygame"], "include_files":includefiles}

setup(name = "Polar Invaders",
      version = "0.1",
      options = {"build_exe":build_exe_options},
      executables = [Executable("Polar Invaders.py", base=base)])
