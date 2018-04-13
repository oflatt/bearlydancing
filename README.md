# Bearly Dancing
![](https://github.com/oflatt/portfolio-gifs/blob/master/beardance.gif)
A rhythm rpg with randomly generated beatmaps, written in python using the pygame library. Journey through a quirky world, playing the music for dance battles between a bear and his foes.

## Setting up the environment

Download a version of python 3.
Run setup.py. Do not run setup.py from IDLE, because there seems to be a bug that causes ultra-slow download speeds.

To play the game without development features, set exportmode in variables.py to True.

## Making an executable

Windows:

Make the absolute path in variables.py go back one folder. Then call *python build.py build*.
A folder named build should appear.

Mac:

Make the absolute path go back two folders. Then call *python build.py bdist_mac --iconfile icon.icns*.
A folder named build should appear. If there are errors in copying files, it may have no effect because of a bug in cx_freeze.



![](https://github.com/oflatt/portfolio-gifs/blob/master/bearly-dancing-demo.gif)


<a rel="license" href="http://creativecommons.org/licenses/by-nc/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc/4.0/88x31.png" /></a><br /><span xmlns:dct="http://purl.org/dc/terms/" property="dct:title">Bearly Dancing</span> by <span xmlns:cc="http://creativecommons.org/ns#" property="cc:attributionName">Oliver Flatt</span> is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc/4.0/">Creative Commons Attribution-NonCommercial 4.0 International License</a>.
