import timeit, statistics
setup1 = '''
for x in range (5):
    a = 0
    a += x
'''

setup2 = '''
for x in range (5):
    a = 0
    a = a + x
'''


print (statistics.mean(timeit.Timer(setup=setup1).repeat(1000, 1000)))
print (statistics.mean(timeit.Timer(setup=setup2).repeat(1000, 1000)))

