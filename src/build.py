from cx_Freeze import setup, Executable
from dependencies import dependencies

dependencieswithoutself = dependencies.copy()
dependencieswithoutself.remove("cx-Freeze")

setup(name='bearly dancing',
      version='0.0',
      options={"build_exe": {"packages":dependencieswithoutself,"include_files":['pics/', 'music/', 'sounds/']}},
      description='A rpg dance adventure by Oliver Flatt.',
      executables = [Executable("bearly dancing.py")])
