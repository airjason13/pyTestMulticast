import logging
import os
from logging.handlers import RotatingFileHandler
FORMAT = '%(asctime)s %(name)-12s %(levelname)s : %(message)s'

def logging_init(s, log_level):
    try:
        logging.basicConfig(level=log_level, format=FORMAT)
        log = logging.getLogger(s)
        os.makedirs('log', exist_ok=True)
        formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)s : %(message)s')
        handler = RotatingFileHandler('log/my_log.log', maxBytes=10**6, backupCount=6)
        handler.setFormatter(formatter)
        log.addHandler(handler)
    except Exception as e:
        print(e)

    #log.basicConfig(level=logging.DEBUG, format=FORMAT)
    return log