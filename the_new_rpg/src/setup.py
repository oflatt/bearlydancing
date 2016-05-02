from cx_Freeze import setup, Executable

setup(name='bigbang',
      version='0.1',
      options={"build_exe": {"packages":["pygame"],}},
      description='A rpg dance adventure by Oliver Flatt on coding, Jacob Valero on maps, Alec Tran and Spirit LR on art.',
      executables = [Executable("bigbang.py")])