#Bearly Dancing
Final project from my programming 1 class

##Setting up the environment
**Important! Make sure python installation is 32 bit and version 3.4**
If running on a school computer, run cmd in administrator mode for installing wheels

Link for download for wheel file of Pygame, call pip install on the wheel file:
<http://www.lfd.uci.edu/~gohlke/pythonlibs/#pygame>

Link for cx_Freeze
https://pypi.python.org/pypi?:action=display&name=cx_Freeze&version=4.3.4
get the 32 bit python 3.4 version of cx freeze

Example of how to change local path variables so you can call pip
set PATH=%PATH%;"C:\Python34"
set PATH=%PATH%;"C:\Python34\scripts"

##How to make the executable
call python setup.py build, a folder called build should appear
then add the correct font to the library folder if there is an error
after that, copy the pics folder over to the folder with the exe file in it
this is a pain but it is more of a pain to fix for now
