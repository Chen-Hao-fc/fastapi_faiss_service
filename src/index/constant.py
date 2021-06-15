# -*- coding: utf-8 -*-      
# --------------------------------------------
# Author: chen hao
# Date: 2021/6/13 17:55 
# Description:  
# --------------------------------------------
import os
pwd = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

INDEX_PATH = f'{pwd}/../resources/trained.index'
FEATURES_PATH = f'{pwd}/../resources/features.pkl'
INIT_VECTORS_PATH = f'{pwd}/../resources/init_vec.tsv'
