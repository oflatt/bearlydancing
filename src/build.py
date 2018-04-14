from cx_Freeze import setup, Executable
from dependencies import dependencies

dependencieswithoutself = dependencies.copy()
dependencieswithoutself.remove("cx-Freeze")

includefiles = ['pics/', 'music/', 'sounds/', 'orangekidregular.ttf', 'icon.png']
includes = []
excludes = ['pathtoself']
myicon = "icon.ico"

from sys import platform
if platform == "darwin":
    dependencieswithoutself.append("AppKit")
    base = None
    myicon = "icon.icns"
    includes.append('pathtoselfmac')
    excludes.append('pathtoselfwindows')
else:
    base = "Win32GUI"
    includes.append('pathtoselfwindows')
    excludes.append('pathtoselfmac')
    
setup(name='bearly dancing',
      version='0.0',
      options={"build_exe": {"packages":dependencieswithoutself,"include_files":includefiles, "includes":includes, "excludes":excludes}},
      description='An rpg dance adventure by Oliver Flatt.',
      executables = [Executable("bearly dancing.py", icon=myicon, base=base)])
