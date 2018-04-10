from cx_Freeze import setup, Executable
from dependencies import dependencies

dependencieswithoutself = dependencies.copy()
dependencieswithoutself.remove("cx-Freeze")

includefiles = ['pics/', 'music/', 'sounds/', 'orangekidregular.ttf']

from sys import platform
if platform == "darwin":
    import os
    os.environ['TCL_LIBRARY'] = '/Library/Frameworks/Tcl.framework/Versions/8.6/Tcl'
    os.environ['TK_LIBRARY'] = '/Library/Frameworks/Tk.framework/Versions/8.6/Tk'
    dependencieswithoutself.append('six')
    dependencieswithoutself.append('appdirs')
    dependencieswithoutself.append('packaging')
    base = None
else:
    base = "Win32GUI"
    
setup(name='bearly dancing',
      version='0.0',
      options={"build_exe": {"packages":dependencieswithoutself,"include_files":includefiles}},
      description='A rpg dance adventure by Oliver Flatt.',
      executables = [Executable("bearly dancing.py", icon="icon.ico", base=base)])
