# -*- coding: utf-8 -*-      
# --------------------------------------------
# Author: chen hao
# Date: 2021/6/13 16:53 
# Description:  
# --------------------------------------------
from fastapi import FastAPI
from index.router import router
from utils.logger import creat_logger

logger = creat_logger('INFO')
app = FastAPI()
app.include_router(router)