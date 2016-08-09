def synctime():
    if not admin.isUserAdmin():
        admin.runAsAdmin()
    else:
        subprocess.Popen(['net', 'start', 'w32time'], creationflags=DETACHED_PROCESS)
        subprocess.Popen(['w32tm', '/resync'], creationflags=DETACHED_PROCESS)

import subprocess
DETACHED_PROCESS = 0x00000008

if __name__ == '__main__':
    import admin
    synctime()
else:
    from . import admin

