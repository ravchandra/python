import logging

def debug_factory(logger, debug_level):
    def custom_debug(msg, *args, **kwargs):
        if logger.level >= debug_level:
           return
        logger._log(debug_level, msg, args, kwargs)
    return custom_debug    

mylogger = logging.Logger('my-logger')
ch = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(funcName)s - %(levelname)s - %(message)s")
ch.setFormatter(formatter)
mylogger.addHandler(ch)

for i in range(1,5):
    logging.addLevelName(logging.DEBUG+i, 'DEBUG%i' % i)
    setattr(mylogger, 'debug%i' % i, debug_factory(mylogger, logging.DEBUG+i))

def from_this_function():
    mylogger.debug('test')
    mylogger.debug1('test2')
    mylogger.debug2('test3')

def from_that_function():
    mylogger.debug('test4')
    mylogger.debug1('test5')
    mylogger.debug2('test6')
    mylogger.debug3('test7')
    
def from_another_function():
    mylogger.debug('asdasd')
    mylogger.debug1('agasdf')
    mylogger.debug2('adasdfa')
    mylogger.debug4('asdfa')
    mylogger.warning('blah')

mylogger.setLevel(logging.DEBUG)
from_this_function()    
mylogger.setLevel(logging.DEBUG+1)
from_that_function()    
mylogger.setLevel(logging.DEBUG+2)
from_another_function() 
