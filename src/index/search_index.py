# -*- coding: utf-8 -*-      
# --------------------------------------------
# Author: chen hao
# Date: 2021/6/13 17:46 
# Description:  
# --------------------------------------------
import mkl
import faiss
import pickle
import numpy as np
from typing import List, Dict
from .constant import INDEX_PATH, FEATURES_PATH
mkl.get_max_threads()

class SearchIndex(object):
    def __init__(self, index_path:str=INDEX_PATH, feature_path:str=FEATURES_PATH):

        assert index_path, "index path is not exists"
        assert feature_path, "feature path is not exists"

        self._index = faiss.read_index(index_path)
        self._features = self.load_features(feature_path)
        self._id2label = {v.id:k for k, v in self._features.items()}

    def load_features(self, path:str):
        with open(path, 'rb') as reader:
            features = pickle.load(reader)
        return features

    def search_by_labels(self, labels:List[str], k:int=5) -> List[Dict]:
        vectors = [self._features[label].vector for label in labels if label in self._features]
        ids = [self._features[label].id for label in labels if label in self._features]
        results = self._search(ids, labels, vectors, k+1)
        return results

    def search_by_vectors(self, vectors:List[float], k:int=5) -> List[Dict]:
        ids = [-1] * len(vectors)
        labels = ['null'] * len(vectors)
        results = self._search(ids, labels, vectors, k)
        return results

    def _search(self, ids:List[int], labels:List[str], vectors:List[float], k:int) -> List[Dict]:
        def pack_neighbor(id, score):
            return {'id':int(id), 'label': str(self._id2label[id]), 'score': float(score)}
        def pack_result(id, label, vector, neighbors):
            return {'id':id, 'label': label, 'vector': vector.tolist(), 'neighbors': neighbors}

        results = []
        vectors = [np.array(vec, dtype=np.float32) for vec in vectors]
        vectors = np.atleast_2d(vectors)

        scores, neighbors = self._index.search(vectors, k) if vectors.size > 0 else ([], [])

        for id, label, vector, score, neighbor in zip(ids, labels, vectors, scores, neighbors):
            neighbor_score = zip(neighbor, score)
            neighbor_score = [(n_id, n_score) for n_id, n_score in neighbor_score if n_id != id and n_id != -1]
            neighbor_score = [pack_neighbor(n_id, n_score) for n_id, n_score in neighbor_score]
            results.append(pack_result(id, label, vector, neighbor_score))

        return results
