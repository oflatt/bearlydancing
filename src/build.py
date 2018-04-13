from cx_Freeze import setup, Executable
from dependencies import dependencies

dependencieswithoutself = dependencies.copy()
dependencieswithoutself.remove("cx-Freeze")

includefiles = ['pics/', 'music/', 'sounds/', 'orangekidregular.ttf', 'icon.png']

from sys import platform
if platform == "darwin":
    dependencieswithoutself.append("AppKit")
    base = None
else:
    base = "Win32GUI"
    
setup(name='bearly dancing',
      version='0.0',
      options={"build_exe": {"packages":dependencieswithoutself,"include_files":includefiles}},
      description='A rpg dance adventure by Oliver Flatt.',
      executables = [Executable("bearly dancing.py", icon="icon.ico", base=base)])
