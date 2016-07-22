import timeit, statistics
setup1 = '''
import subprocess
DETACHED_PROCESS = 0x00000008
subprocess.Popen(["shutdown", "-r", "-t", "5000"],creationflags=DETACHED_PROCESS)
'''

setup2 = '''
print ('abc')
'''


print (statistics.mean(timeit.Timer(setup=setup1).repeat(1000, 1000)))
print (statistics.mean(timeit.Timer(setup=setup2).repeat(1000, 1000)))

