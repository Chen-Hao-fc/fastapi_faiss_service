# -*- coding: utf-8 -*-      
# --------------------------------------------
# Author: chen hao
# Date: 2021/6/13 17:45 
# Description:  
# --------------------------------------------
import faiss
import pickle
import numpy as np
from dataclasses import dataclass
from typing import List, Dict, Tuple
from .constant import INIT_VECTORS_PATH, INDEX_PATH, FEATURES_PATH

@dataclass
class Feature:
    id: int
    label: str
    vector: List[float]

class BuildIndex(object):
    def __init__(self, path: str=INIT_VECTORS_PATH):
        assert path, 'init vectors path is not exists'
        self.init_vectors_path = path
        self.run()

    def read_tsv(self, vec_sep=',') -> Tuple[List[List[float]], Dict[str, Feature]]:
        vectors = []
        features = {}
        number = 0
        with open(self.init_vectors_path, 'r') as reader:
            line = reader.readline()
            while line:
                content = line.strip().split('\t')
                if len(content) != 2:
                    line = reader.readline()
                    continue
                label = content[0]
                vector = [float(v) for v in content[1].strip().split(vec_sep)]
                features[label] = Feature(label=label, id=number, vector=vector)
                vectors.append(vector)
                number += 1
                line = reader.readline()
        return vectors, features

    def write_tsv(self, features: Dict[str, Feature]):
        with open(self.init_vectors_path, 'w') as writer:
            for label, feature in features.items():
                writer.write(label + '\t' + ','.join([str(v) for v in feature.vector] + '\n'))

    def __dump_features(self, features:Dict[str, Feature]):
        with open(FEATURES_PATH, 'wb') as writer:
            pickle.dump(features, writer)

    def __build_index(self, vectors:List[List[float]]):
        vectors = np.array(vectors, dtype=np.float32)
        dim = vectors.shape[-1]

        # index = faiss.index_factory(dim, "IVF4096,Flat")
        # index.train(vectors)
        index = faiss.IndexFlatL2(dim)
        index.add(vectors)

        faiss.write_index(index, INDEX_PATH)

    def run(self):
        vectors, features = self.read_tsv()
        self.__build_index(vectors)
        self.__dump_features(features)

    @classmethod
    def update(cls):
        path = INIT_VECTORS_PATH
        ins = cls(path)
        ins.run()

    def add_vector(self, label:str, vector:List[float]):
        vectors, features = self.read_tsv()
        dim = len(vectors[0])
        if len(vector) != dim:
            return
        if label not in features:
            features[label] = vector
            self.write_tsv(features)
