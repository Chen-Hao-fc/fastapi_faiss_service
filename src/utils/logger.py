# -*- coding: utf-8 -*-      
# --------------------------------------------
# Author: chen hao
# Date: 2021/6/13 19:36 
# Description:  
# --------------------------------------------
import logging
import logging.handlers
from logging import getLogger

def creat_logger(level=logging.DEBUG):
    logger = getLogger()
    formatter = logging.Formatter(
        '[%(levelname)s] - [%(asctime)s] - [pid:(process)d] - [%(pathname)s line:%(lineno)s] - %(message)s'
    )

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(level)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    logger.setLevel(level)

    file_handler = logging.FileHandler('service.log', encoding='utf-8')
    file_handler.setFormatter(formatter)
    file_handler.setLevel(level)
    logger.addHandler(file_handler)
    logger.setLevel(level)

    return logger