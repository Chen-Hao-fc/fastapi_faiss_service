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
mkl.get_max_threads()

class SearchIndex(object):
    def __init__(self, index_path, feature_path):

        assert index_path, "index path is not exists"
        assert feature_path, "feature path is not exists"

        self.__index = faiss.read_index(index_path)
        self.__features = self.load_features(feature_path)
        self.__id2label = {v.id:k for k, v in self.__features.items()}

    def load_features(self, path):
        with open(path, 'rb') as reader:
            features = pickle.load(reader)
        return features

    def search_by_labels(self, labels, k):
        vectors = [self.__features[label].vector for label in labels if label in self.__features]
        ids = [self.__features[label].id for label in labels if label in self.__features]
        results = self.__search(ids, labels, vectors, k+1)
        return results

    def search_by_vectors(self, vectors, k):
        ids = [None] * len(vectors)
        labels = [None] * len(vectors)
        results = self.__search(ids, labels, vectors, k)
        return results

    def __search(self, ids, labels, vectors, k):
        def pack_neighbor(id, score):
            return {'id':id, 'label': self.__id2label[id], 'score': score}
        def pack_result(id, label, vector, neighbors):
            return {'id':id, 'label': label, 'vector': vector.tolist(), 'neighbors': neighbors}


        results = []
        vectors = [np.array(vec, dtype=np.float32) for vec in vectors]
        vectors = np.atleast_2d(vectors)

        scores, neighbors = self.__index.search(vectors, k) if vectors.size > 0 else ([], [])

        for id, label, vector, score, neighbor in zip(ids, labels, vectors, scores, neighbors):
            neighbor_score = zip(neighbor, score)
            neighbor_score = [(n_id, n_score) for n_id, n_score in neighbor_score if n_id != id and n_id != -1]
            neighbor_score = [pack_neighbor(n_id, n_score) for n_id, n_score in neighbor_score]
            results.append(pack_result(id, label, vector, neighbor_score))

        return results
