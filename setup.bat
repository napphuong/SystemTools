rem *** Used to create a Python exe 

rem ***** create the exe
cd system tools
setup.py py2exe

rem **** pause so we can see the exit codes
pause "done...hit a key to exit"