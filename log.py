import logging

logger = logging.getLogger("project")
logger.setLevel(logging.DEBUG)

formatter1 = logging.Formatter('%(asctime)s - %(name)s -\
 %(pathname)s - %(funcName)s - %(lineno)s - %(levelname)s - %(message)s')

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter1)
logger.addHandler(ch)

fh = logging.FileHandler('test.log')
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter1)
logger.addHandler(fh)
