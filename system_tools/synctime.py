import admin, subprocess
DETACHED_PROCESS = 0x00000008
def synctime():
    if not admin.isUserAdmin():
        admin.runAsAdmin()
    else:
        subprocess.Popen(['net', 'start', 'w32time'], creationflags=DETACHED_PROCESS)
        subprocess.Popen(['w32tm', '/resync'], creationflags=DETACHED_PROCESS)

if __name__ == '__main__':
    synctime()
        
