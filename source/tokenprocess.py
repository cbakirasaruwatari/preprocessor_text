from __future__ import unicode_literals
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import functools
import re
import json
import pathlib
import os
import sys
import subprocess
import shlex
import itertools
from collections import Counter
from dataclasses import dataclass,asdict
from util import getter,setter,config,flatten
from typing import Optional,Union,NewType,Tuple, List, Any, Dict, Callable, Generic, NoReturn

import numpy as np

class TokenProcess():
    # CORPUS_OUTPUT_PATH = "../data/twitter_data_corpus/corpus.txt"
    TFIDF_OUTPUT_PATH = "../data/twitter_data_tfidf"
    token:list=None
    
    class TfIdf():
        class Tf():
            @classmethod
            def binary(self,doc:list) -> dict:
                return {w:1 for w in list(set(doc))}
            @classmethod
            def raw_count(self,doc:list) -> dict:
                freq:list = Counter(doc).most_common()
                return {r[0]:r[1] for r in freq}
            @classmethod
            def term_frequency(self,doc:list) -> dict:
                freq:list = Counter(doc).most_common()
                max_count:int = max([row[1] for row in freq])
                return {r[0]:r[1]/max_count for r in freq}
            @classmethod
            def term_frequency_sum(self,doc:list) -> dict:
                freq:list = Counter(doc).most_common()
                all_count:int = sum([row[1] for row in freq])
                return {r[0]:r[1]/all_count for r in freq}   
            @classmethod
            def log_normalization(self,doc:list) -> dict:
                freq:list = Counter(doc).most_common()
                return {r[0]:np.log10(r[1] + 1) for r in freq}
            @classmethod
            def double_normalization(self,doc:list,k:int=0.5) -> dict:
                freq:list = Counter(doc).most_common()
                max_count:int = max([row[1] for row in freq])
                return {r[0]:k + ((1-k) * r[1] / max_count) for r in freq}

        class Idf():
            def __init__(self,doc_list: list,idf_weight_topn:int=1000) -> None:
                self.doc_list=doc_list
                self.idf_weight_topn=idf_weight_topn
            def unary(self):
                pass
            def normal(self):
                pass
            def smooth(self):
                pass
            def max(self):
                pass
            def probabilistic(self):
                pass
            def calc_insta(self):
                doc_list_ordered = []
                for doc in self.doc_list:
                    doc_list_ordered.append([token[0] for token in Counter(flatten(doc)).most_common()])
                doc_count = len(self.doc_list)
                i = 0
                ret = {}
                for word,count in Counter(flatten(doc_list_ordered)).items():
                    if i < self.idf_weight_topn:
                        ret.update({word:np.log10(doc_count / count+1)})
                    else:
                        ret.update({word:np.log10(2)})
                    i += 1
                return ret
                
            
            def normalize(self):
                pass
        
        def run(self):
            pass

        def run_zhang(self,*doc) -> dict:
            pass

    class Distribution():
        def __init__(self,vectype:str):
            self.vectype = vectype

        @getter
        def vectype(self) -> str:
            return self._vectype
        @setter
        def vectype(self,vectype:str) -> NoReturn:
            if vectype == "fasttext":
                self._vectype = vectype
            else:
                raise NotImplementedError("just use fasttext")

        def to_vec(self,input,output,**optional) -> NoReturn:
            option = " ".join(["-" + k + " " + v for k,v in  optional.items()])            
            config = " -input " + input + " -output " + output + option
            try:
                subprocess.call(shlex.split(config))
            except Exception as e:
                print(e)
                sys.exit()

    def tfidf(self) -> NoReturn:
        tfs,idf,tfidf = self.tfidf.run_zhang()
        with open(tfidf_dir + "tfidf.json","w") as f:
            json.dump(self.tfidf.run_zhang(),f,indent=4,ensure_ascii=False)

    def corpus(self,input,output) -> NoReturn:
        inputpath = pathlib.Path(input)
        outputparh = pathlib.Path(output + "/corpus")
        if not inputpath.exists():
            raise FileNotFoundError("There is no file you input:" + str(inputpath))
        elif outputparh.exists():
            raise FileExistsError("already exist:" + str(outputparh))
        if inputpath.is_file():
            pass
        elif inputpath.is_dir():
            for filename in inputpath.iterdir():
                with open(filename) as r,open(outputparh,"a+") as w:
                    w.write(" ".join(filter(lambda x: x != "<BOS>",["\n" if word == "<EOS>" else word for word in json.load(r)])))

    def frequency(self,input,output) -> NoReturn:
        inputpath = pathlib.Path(input)
        outputparh = pathlib.Path(output)
        for filename in inputpath.iterdir():
            with open(outputparh / filename.name,"w") as w, open(filename) as r:
                json.dump(Counter(json.load(r)).most_common(),w,indent=4,ensure_ascii=False)
                

    def skipgram(self,input,output) -> NoReturn:
        print(input)
        print(output)
        fasttext_dir="../fastText"
        os.chdir(fasttext_dir)
        subprocess.call(shlex.split("./fasttext skipgram -input ../source/twitter_sample2/corpus/corpus -output ./aaaa -minCount 10 -epoch 10 -neg 100"))

