# SystemTools

# Issues

2016.07.23: time sync only work with some trick (add import synctime in system_tools.pyw)
2016.07.23: Turnoff screen only work with 1.5 seconds delay
2016.07.22: [SOLVED] should only ask for admin right when sync time
2016.07.22: [SOLVED] pywin32 module cannot be complied
2016.07.21: Progress bar now can't work
2016.07.21: Should add global shortcuts
2016.07.21: Should refresh app buttons after adding apps
2016.07.21: [SOLVED] Should add button to turn off the screen
2016.07.21: Should detect power plan and change combobox value
2016.07.20: [SOLVED] Should check if this app is running when start
2016.01.06: [SOLVED] Don't know how to ask AUC permission

# Change Logs:
	synctime is moved to admin module
	not copy config.ini when run setup.py
	re-ogarnize folder
	change setup.py and setup.bat location
	change distribution folder location

20160723:
	add turnoff screen button
	only ask for admin right when needed
	sync time now trigger by a button with a little trick

20160722:
	icon folder and config.ini now are auto copied by setup.py file
	pywin32 can be complied by changing setup.py file (bundle = 1 to 3)
	improve setup.py code
	Only run if app is not running
	Add icon to main app
	Add setup.bat to create py2exe with only one click

20160720:	
	Restructure the code
	Resync system time on startup
	Add buttons to run favourite apps separately
	Add AUC on startup
	Add setup.py to run py2exe
	Textbox now save data to settings.ini when lost focus
	Remove console window when run system command
	App is minimized to tray now

20160527: 
	Initial Release