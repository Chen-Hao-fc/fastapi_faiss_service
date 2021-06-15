# -*- coding: utf-8 -*-      
# --------------------------------------------
# Author: chen hao
# Date: 2021/6/14 10:23 
# Description:  
# --------------------------------------------
import json
from typing import List
from .build_index import BuildIndex
from fastapi import APIRouter, Query
from .search_index import SearchIndex
from .constant import INIT_VECTORS_PATH
from fastapi.encoders import jsonable_encoder

router = APIRouter()
search = None

@router.on_event('startup')
async def start_up():
    print('=' * 100)
    BuildIndex(INIT_VECTORS_PATH)
    print('=' * 100)
    global search
    search = SearchIndex()

@router.get('/index/labels')
async def read_item(k:int, labels:str):
    global search
    labels = labels.split(',')
    result = search.search_by_labels(labels, k)

    return jsonable_encoder(result)

@router.get('/index/vectors')
async def read_item(k:int, vectors:str):
    global search
    vectors = [float(v) for v in vectors.split(',')]
    result = search.search_by_vectors(vectors, k)

    return jsonable_encoder(result)
