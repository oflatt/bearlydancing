from cx_Freeze import setup, Executable
from dependencies import dependencies

dependencieswithoutself = dependencies.copy()
dependencieswithoutself.remove("cx-Freeze")

includefiles = ['pics/', 'music/', 'sounds/', 'orangekidregular.ttf', 'icon.png']
includes = []
excludes = ['pathtoself']
myicon = "icon.ico"

import imp
import os
MODULE_EXTENSIONS = ('.py', '.pyc', '.pyo')

def package_contents(package_name):
    file, pathname, description = imp.find_module(package_name)
    if file:
        raise ImportError('Not a package: %r', package_name)
    # Use a set because some may be both source and compiled.
    return [os.path.splitext(module)[0]
        for module in os.listdir(pathname)
        if module.endswith(MODULE_EXTENSIONS) and module != "init.py"]


from sys import platform
if platform == "darwin":
    dependencieswithoutself.remove("pyobjc")
    dependencieswithoutself.append("AppKit")
    base = None
    myicon = "icon.icns"
    includes.append('pathtoselfmac')
    excludes.append('pathtoselfwindows')
    packagingcontent = package_contents('packaging')
    for x in range(len(packagingcontent)):
        packagingcontent[x] = "packaging." + packagingcontent[x]
    includes.extend(packagingcontent)
else:
    base = "Win32GUI"
    includes.append('pathtoselfwindows')
    excludes.append('pathtoselfmac')
    
setup(name='bearly dancing',
      version='0.0',
      options={"build_exe": {"packages":dependencieswithoutself,"include_files":includefiles, "includes":includes, "excludes":excludes}},
      description='An rpg dance adventure by Oliver Flatt.',
      executables = [Executable("bearly dancing.py", icon=myicon, base=base)])
