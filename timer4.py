import timeit
import time
def gettime(f):
    def wrapped():
        start = timeit.default_timer()
        f()
        end = timeit.default_timer()
        return end-start
    return wrapped

@gettime
def myf():
    time.sleep(5)

myf()
