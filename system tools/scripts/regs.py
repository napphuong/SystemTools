def restorereg():
    subprocess.Popen(['reg', 'import', '.\\regs\\globalpowerpolicy.reg'], creationflags=DETACHED_PROCESS)
    subprocess.Popen(['reg', 'import','.\\regs\\usershellfolder.reg'], creationflags=DETACHED_PROCESS)

def backupreg():
    subprocess.Popen(['reg','export','HKCU\\Control Panel\\PowerCfg\\GlobalPowerPolicy','.\\regs\\globalpowerpolicy.reg', '/y'],creationflags=DETACHED_PROCESS)
    subprocess.Popen(['reg','export','HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer\\User Shell Folders','.\\regs\\usershellfolder.reg','/y'],creationflags=DETACHED_PROCESS)
    
import subprocess
DETACHED_PROCESS = 0x00000008

if __name__ == '__main__':
    print ('a')
    exportreg
