import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter1 = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

formatter2 = logging.Formatter('%(asctime)s - %(name)s -\
 %(pathname)s - %(funcName)s - %(lineno)s - %(levelname)s - %(message)s')

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter1)
logger.addHandler(ch)

fh = logging.FileHandler('test.log')
fh.setLevel(logging.WARN)
fh.setFormatter(formatter2)
logger.addHandler(fh)

def test_func():
    logger.debug('debug message')
    logger.info('info message')
    logger.warn('warn message')
    logger.error('error message')
    logger.critical('critical message')

test_func()
