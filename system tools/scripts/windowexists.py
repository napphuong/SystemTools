import win32api, win32ui

def windowexists(windowName):
    try:
        win32ui.FindWindow(None, windowName)
    except win32ui.error:
        return False
    else:
        return True

if __name__ == '__main__':
    if WindowExists ('System Tools by Napphuong'):
        print ("yes")
    else:
        print ("no")