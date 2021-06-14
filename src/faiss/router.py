# -*- coding: utf-8 -*-      
# --------------------------------------------
# Author: chen hao
# Date: 2021/6/14 10:23 
# Description:  
# --------------------------------------------
import json
from typing import List
from fastapi import APIRouter
from .build_index import BuildIndex
from .search_index import SearchIndex
from .constant import INIT_VECTORS_PATH
from fastapi.encoders import jsonable_encoder


router = APIRouter()
search = None

@router.on_startup
async def start_up():
    BuildIndex(INIT_VECTORS_PATH)
    global search
    search = SearchIndex()

@router.get('/faiss')
async def read_item(labels:List[str], k:int):
    global search
    result = search.search_by_labels(labels, k)

    return jsonable_encoder(result)

@router.get('/faiss')
async def read_item(vectors:json, k:int):
    global search
    vectors = json.loads(vectors)['v']
    result = search.search_by_vectors(vectors, k)

    return jsonable_encoder(result)
