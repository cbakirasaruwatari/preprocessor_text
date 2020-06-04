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
from util import getter,setter,flatten,load_json
from typing import Optional,Union,NewType,Tuple, List, Any, Dict, Callable, Generic, NoReturn
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer,CountVectorizer


class TokenProcess():    
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
        
        # def run(self) -> dict:
        #     pass

        @classmethod
        def run_zhang(cls,*doc) -> dict:
            pass

        @classmethod
        def run(cls,input: pathlib.Path,output: pathlib.Path):

            inputpathes = list(input.iterdir())
            docs = [" ".join(load_json(file)) for file in inputpathes]
            count_vectorizer = CountVectorizer()
            count_fit = count_vectorizer.fit_transform(docs)
            tfidf_vectorizer = TfidfVectorizer(token_pattern='(?u)\\b\\w+\\b',lowercase=False)
            tfidf_fit = tfidf_vectorizer.fit_transform(docs)
            tokens = tfidf_vectorizer.get_feature_names()

            with open(output / pathlib.Path("labels.json"),"w") as f:
                json.dump([str(path) for path in inputpathes], f, indent=4)
            with open(output / pathlib.Path("count_vectorizer.pickle"),"wb") as f:
                pickle.dump(count_vectorizer, f)            
            with open(output / pathlib.Path("count_vectorizer.pickle"),"wb") as f:
                pickle.dump(count_vectorizer, f)
            with open(output / pathlib.Path("count_fit.pickle"),"wb") as f:
                pickle.dump(count_fit, f)
            with open(output / pathlib.Path("tfidf_vectorizer.pickle"),"wb") as f:
                pickle.dump(tfidf_vectorizer, f)
            with open(output / pathlib.Path("tfidf_fit.pickle"),"wb") as f:
                pickle.dump(tfidf_fit, f)
            os.mkdir(output / pathlib.Path("docs"))            
            for vec,doc in zip(tfidf_fit.toarray(),[str(path) for path in inputpathes]):
                pd.DataFrame(data={"token":[tokens[i] for i in np.nonzero(vec)[0].astype(int)]}, index=np.nonzero(vec)[0].astype(int)).assign(score=vec[np.nonzero(vec)]).sort_values("score",ascending=False).to_csv(output / pathlib.Path("docs") / pathlib.Path(pathlib.Path(doc).stem + ".csv"))
                # print(np.array([np.nonzero(vec)[0].astype(int),vec[np.nonzero(vec)]]))
                # np.savetxt(output / pathlib.Path("i") / pathlib.Path(pathlib.Path(doc).stem + ".csv"),np.array([np.nonzero(vec)[0].astype(int),vec[np.nonzero(vec)]]).T , fmt='%i', delimiter=",",)
                # np.savetxt(output / pathlib.Path("v") / pathlib.Path(pathlib.Path(doc).stem + ".csv"), vec[np.nonzero(vec)])
                # df = pd.DataFrame(data=X_count.toarray(),
                # columns=count_vectorizer.get_feature_names())


            # 見やすさのために表示するときは pandas のデータフレームにする
            # df = pd.DataFrame(data=X_count.toarray(),
            # columns=count_vectorizer.get_feature_names())

            # IDF を表示する
            # print('--- IDF (Inverse Document Frequency) ---')
            # df = pd.DataFrame(data=[tfidf_vectorizer.idf_],
            #                 columns=tfidf_vectorizer.get_feature_names())
            # print(df)
            # df.to_csv('twitter_sample2/others/idf.csv')
            # TF-IDF を表示する
            # print('--- TF-IDF ---')
            # df = pd.DataFrame(data=X_tfidf.toarray(),
            #                 columns=tfidf_vectorizer.get_feature_names())
            # print(df)
            
   
            # df.to_csv('twitter_sample2/others/tfidf.csv')


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

    # CORPUS_OUTPUT_PATH = "../data/twitter_data_corpus/corpus.txt"
    TFIDF_OUTPUT_PATH = "../data/twitter_data_tfidf"
    token:list=None


    def tfidf(self,input,output) -> pathlib.Path:
        self.TfIdf.run(input,output)
    

    # def tfidf(self) -> NoReturn:
    #     tfs,idf,tfidf = self.tfidf.run_zhang()
    #     with open(tfidf_dir + "tfidf.json","w") as f:
    #         json.dump(self.tfidf.run_zhang(),f,indent=4,ensure_ascii=False)

    def corpus(self,input,output) -> pathlib.Path:
        print("create corpus...")
        if (outputpath := (output / pathlib.Path("corpus"))).exists():
            raise FileExistsError("already exist:" + str(outputpath))
        for inputpath in input.iterdir():
            with open(inputpath) as r,open(outputpath,"a+") as w:
                w.write(" ".join(filter(lambda x: x != "<BOS>",["\n" if word == "<EOS>" else word for word in json.load(r,strict=False)])))
        return outputpath
    
    def frequency(self,input,output) -> NoReturn:
        for filename in input.iterdir():
            with open(output / filename.name,"w") as w, open(filename) as r:
                json.dump(Counter(json.load(r)).most_common(),w,indent=4,ensure_ascii=False)
                

    def skipgram(self,input,output) -> NoReturn:
        fasttext_dir="../fastText"
        os.chdir(fasttext_dir)
        subprocess.call(shlex.split("./fasttext skipgram -input " + str(input) + "/corpus" + " -output " + str(output) + "/skipgram" + " -minCount 10 -epoch 10 -neg 100"))
        os.chdir("../source")

