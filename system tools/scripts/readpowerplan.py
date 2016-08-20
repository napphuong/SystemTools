import winreg
POWER_SAVER = 0
HIGH_PERFORMANCE = 1
BALANCED = 2
def readpowerplan():
    root_key=winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 'SYSTEM\\CurrentControlSet\\Control\\Power\\User\\PowerSchemes', 0, winreg.KEY_READ)
    [keyValue,regType]=(winreg.QueryValueEx(root_key,'ActivePowerScheme'))
    winreg.CloseKey(root_key)
    if keyValue == 'a1841308-3541-4fab-bc81-f71556f20b4a':
        return POWER_SAVER
    elif keyValue =='8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c':
        return HIGH_PERFORMANCE
    elif keyValue == '381b4222-f694-41f0-9685-ff5bb260df2e':
        return BALANCED

if __name__ == '__main__':
    print (readpowerplan())
