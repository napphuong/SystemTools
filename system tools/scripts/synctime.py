def synctime():
    if not admin.isUserAdmin():
        admin.runAsAdmin()
    else:
        DETACHED_PROCESS = 0x00000008
        subprocess.Popen(['net', 'start', 'w32time'], creationflags=DETACHED_PROCESS)
        subprocess.Popen(['w32tm', '/resync'], creationflags=DETACHED_PROCESS)

import subprocess
if __name__ == '__main__':
    import admin
    synctime()
else:
    from . import admin

