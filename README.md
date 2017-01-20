#Bearly Dancing

##Setting up the environment
**Important! Make sure python installation is 32 bit and version 3.4.4**

Pick wheel files that say cp 34 and win32 when downloading. To install wheel files call pip install on them, and make sure that pip is up to date.

Link for Pygame:
<http://www.lfd.uci.edu/~gohlke/pythonlibs/#pygame>

Link for cx_Freeze:
https://pypi.python.org/pypi?:action=display&name=cx_Freeze&version=4.3.4

Link for numpy:
http://www.lfd.uci.edu/~gohlke/pythonlibs/#numpy

Example of how to change local path variables so you can call pip
set PATH=%PATH%;"C:\Python34"
set PATH=%PATH%;"C:\Python34\scripts"

##Setting up pyFluidSynth
Get visual studio for a c compiler, located for example:
"c:\Program Files (x86)\Microsoft Visual Studio 14.0\vc\vcvarsall.bat"

##How to make the executable
call python setup.py build, a folder called build should appear
then add the correct font to the library folder if there is an error
after that, copy the pics folder over to the folder with the exe file in it
this is a pain but it is more of a pain to fix for now
