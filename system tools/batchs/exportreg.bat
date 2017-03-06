rem *** power settings (lid action) notworking :((
reg export "HKLM\SYSTEM\ControlSet001\Control\Power\User\PowerSchemes" "./regs/PowerSchemes1.reg" /y
reg export "HKLM\SYSTEM\CurrentControlSet\Control\Power\User\PowerSchemes" "./regs/PowerSchemes2.reg" /y

rem *** power (fastboot)
reg export "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Power" "./regs/Power2.reg" /y
reg export "HKLM\SYSTEM\ControlSet001\Control\Session Manager\Power" "./regs/Power1.reg" /y

rem *** time and timezone
reg export "HKLM\SYSTEM\CurrentControlSet\Services\tzautoupdate" "./regs/tzautoupdate.reg" /y
reg export "HKLM\SYSTEM\CurrentControlSet\Services\W32Time" "./regs/W32Time.reg" /y

rem *** folder settings
reg export "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders" "./regs/UserShellFolders.reg" /y

set /p DUMMY=Hit ENTER to continue...