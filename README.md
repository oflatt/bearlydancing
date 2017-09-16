#Bearly Dancing#

##Setting up the environment##

Download a version of python 3, and add it to PATH.

Call pip install on necessary libraries: numpy, pygame, cx_Freeze


Example of how to change local path variables so you can call pip
set PATH=%PATH%;"C:\Python34"
set PATH=%PATH%;"C:\Python34\scripts"

##How to make the executable##
call python setup.py build, a folder called build should appear
then add the correct font to the library folder if there is an error
after that, copy the pics folder over to the folder with the exe file in it
this is a pain but it is more of a pain to fix for now
