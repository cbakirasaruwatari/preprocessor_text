from __future__ import unicode_literals
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import random
import json
import re
import logging
import time
import traceback
import configparser
from abc import ABCMeta, abstractmethod
import inspect
import re
import unicodedata
import functools
import pathlib
import math
# from collections import namedtuple
import queue
from preprocessor_base import TextPreprocessor
from preprocessor_log import clslog
from util import load_json,load_yaml
from logging import getLogger
import pickle
import numpy as np
import pandas as pd
from tqdm import tqdm
# from sklearn.feature_extraction.text import TfidfVectorizer,CountVectorizer


logger = getLogger(os.path.abspath(__file__))

@clslog(logger)
class PreprocessorTextTwitter(TextPreprocessor):
    def __init__(self,yaml_path):
        super().__init__("twitter",yaml_path)

    def user_to_vector(self):
        for path in self.project.resource_path.iterdir():
            print(str(path) + " processing to token...")
            with open(path) as f:
                result = []
                for post in json.load(f):
                    result = result + self._process_text(json.loads(post["post"])["text"])
                with open(self.project.destination_path["text_mecab"] / pathlib.Path(path.stem + ".json"),"w") as w:
                    json.dump(result,w,indent=4,ensure_ascii=False)
        self._process_token()
        self._calc_avg_vectors()

    def _calc_avg_vectors(self):
        output_path = self.project.destination_path["result"] / pathlib.Path("_result.vec")
        if os.path.exists(output_path):
            raise FileExistsError
        # TODO stop_wardsに入っているものは計算から除外する
        stop_wards = ["<BOS>","<EOS>","する","てる","なる","ある","の","ない","いる","RT","れる","の","もの","せる","これ","てる","こと","ん","それ"]
        # read skipgram
        vector_path = self.project.destination_path["token_skipgram"] / pathlib.Path("skipgram.vec")
        with open(vector_path) as r:
            for line in r:
                header = line.split()
                break
        tokens = np.loadtxt(vector_path,dtype=str,skiprows=1,usecols=0)
        vectors = np.loadtxt(vector_path,skiprows=1,usecols=[i for i in range(1, 101)])
        print('dims: ' + header[1] +  ', vocs: ' + header[0])    
        if vectors.shape[0] != int(header[0]) or vectors.shape[1] != int(header[1]):
            raise Exception()

        with open(output_path,"a") as w:
            tfidf_files = [v for v in (self.project.destination_path["token_tfidf"] /  pathlib.Path("docs/")).iterdir()]
            output_header = str(len(tfidf_files)) + " " + str(header[1]) + "\n"
            w.write(output_header)
            for file in tfidf_files:
                stop_wards = ["BOS","EOS","する","てる","なる","ある","の","ない","いる","RT","れる","の","もの","せる","これ","てる","こと","ん","それ"]
                ds = pd.read_csv(file).query('token not in ' + str(stop_wards)).token.values.tolist()
                # print(str(file) + " processing to user vector...")
                if len(ds) < 100:
                    continue
                try:
                    user_vec = np.mean([(vectors[np.where(tokens == d[0])]).astype(float) for d in ds[0:99] if len(vectors[np.where(tokens == d[0])]) != 0],axis=0)
                    w.write(pathlib.Path(file).stem + " ")
                    np.savetxt(w,user_vec,delimiter=' ')
                except Exception as e:
                    print(e)
                    print(file)
                    continue

    
    def _process_text(self,text):
        result = self.text_processor.set(text).normalize().remove_emoji().remove_url().remove(
            "tag",
            "reply",
            "rt",
            "user_at"
        ).mecab()
        return result
    
    def _process_token(self):
        for process in self.project.processes["token"]:
            if process == "skipgram":
                getattr(self.token_processor,process)(self.project.destination_path["token_corpus"],self.project.destination_path["token_" + process])
            else:
                getattr(self.token_processor,process)(self.project.destination_path["text_mecab"],self.project.destination_path["token_" + process])
    
    def _cluster_user_vector(self):
        raise NotImplementedError
    
    def run(self):
        raise NotImplementedError

if __name__ == "__main__":

    text = PreprocessorTextTwitter("config.yml")
    text.user_to_vector()
    # text.tfidf()
