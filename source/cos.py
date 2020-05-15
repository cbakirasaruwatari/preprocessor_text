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
from typing import (Any)
from dataclasses import dataclass
from collections import namedtuple
import shlex
import subprocess


import MeCab
import emoji
import neologdn

class PreprocessorText():
    
    _texts=None
    def run(self,*func):
        '''
        # pass functions. 
        '''     
        for func in func:
            func()

    def normalize(self) -> functools.partial:
        '''
        # see https://github.com/neologd/mecab-ipadic-neologd/wiki/Regexp.ja#python-written-by-hideaki-t--overlast
        '''        
        return functools.partial(self.__normalize)

    def __normalize(self) -> None:
        self._texts = [neologdn.normalize(text) for text in self._texts]

    def remove_emoji(self) -> functools.partial:
        '''
        # All emoji must be deleted in the text.
        '''        
        return functools.partial(self.__remove_emoji)

    def __remove_emoji(self) -> None:
        self._texts = [''.join(c for text in self._texts for c in text if c not in emoji.UNICODE_EMOJI)]

    def remove_url(self) -> functools.partial:
        '''
        # All url must be deleted in the text.
        '''
        return functools.partial(self.__remove_url)

    def __remove_url(self) -> None:
        exp = re.compile(r"http\S+")
        self._texts = [exp.sub("",text) for text in self._texts]

    def set_for_tokenize(self) -> functools.partial:
        return functools.partial(self.__set_for_tokenize)

    def __set_for_tokenize(self) -> None:
        self._texts = [text.replace("\n", " ") for text in self._texts]

    def dump_as_tokens(self,path) -> None:
        tokenizer = MeCab.Tagger ('-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd')
        tokenizer.parse('')
        result = []
        for text in self._texts:
            node = tokenizer.parseToNode(text)
            keywords = []
            while node:
                if node.feature.split(",")[0] == u"名詞":
                    keywords.append(node.surface)
                if node.feature.split(",")[0] == u"固有名詞":
                    keywords.append(node.surface)
                elif node.feature.split(",")[0] == u"形容詞":
                    keywords.append(node.feature.split(",")[6])
                elif node.feature.split(",")[0] == u"動詞":
                    keywords.append(node.feature.split(",")[6])
                node = node.next
            if len(keywords) >= 5: 
                result.append(keywords)
        with open(path,"w") as f:
            json.dump(result,f,indent=4,ensure_ascii=False)
    
class PreprocessorTextTwitter(PreprocessorText):
    class option():
        def __init__(self):
            self.remove_rt = self.remove_rt()
        @dataclass
        class remove_rt:
            @dataclass(frozen=True)
            class cons:
                RT_PATTERN_FORMAL: str=r"(^(?:RT\s@.+:\s))"
                RT_PATTERN_INFORMAL: str=r"(^(?:RT\s@.+:\s))"
            informal: bool=False
            def __setattr__(self, name:str,value: Any) -> None:
                if name.islower() is False:
                    msg = "option must be lower case:" + name
                    raise ValueError(msg)
                if hasattr(self,name) is False:
                    msg = str(self.__class__.__name__) + " has no " + "'" + name + "'" + " option"
                    raise KeyError(msg)
                super().__setattr__(name, value)        
    _options = option()

    def __init__(self,texts:list) -> None:
        self._texts = texts

    def remove_rt(self,**options:dict) -> functools.partial:
        '''
        # All url must be deleted in the text().
        '''        
        return functools.partial(self.__remove_rt,o=options)
    
    def __remove_rt(self,o:dict) -> None:
        for k,v in o.items():
            setattr(self._options.remove_rt,k,v)
        if self._options.remove_rt.informal == False:
            exp = re.compile(self._options.remove_rt.cons.RT_PATTERN_FORMAL,flags=re.MULTILINE | re.DOTALL)
        else:
            exp = re.compile(self._options.remove_rt.cons.RT_PATTERN_INFORMAL,flags=re.MULTILINE | re.DOTALL)
        self._texts = [exp.sub("",text) for text in self._texts]

    def remove_tag(self) -> functools.partial:
        '''
        # All tag must be deleted in the text.
        '''          
        return functools.partial(self.__remove_tag)

    def __remove_tag(self) -> None:
        exp = re.compile(r'(#[^\s]+)',flags=re.MULTILINE | re.DOTALL)
        self._texts = [exp.sub("",text) for text in self._texts]

    def remove_reply(self) -> functools.partial:
        '''
        # All reply and mention must be deleted in the text.
        '''
        return functools.partial(self.__remove_reply)

    def __remove_reply(self) -> None:    
        exp = re.compile(r"^@([A-Za-z0-9_]+) ",flags=re.MULTILINE | re.DOTALL)
        self._texts = [exp.sub("",text) for text in self._texts]

    def remove_user_at(self) -> functools.partial:
        '''
        # All user must be deleted in the text.
        '''        
        return functools.partial(self.__remove_user_at)
     
    def __remove_user_at(self) -> None:
        exp = re.compile(r"@([A-Za-z0-9_]+)",flags=re.MULTILINE | re.DOTALL)
        self._texts = [exp.sub("",text) for text in self._texts]

def to_fasttext(fasttext_dir="../fastText"):
    os.chdir(fasttext_dir)
    # subprocess.call(shlex.split("./fasttext skipgram -input ../data/twitter_data_corpus/corpus -output ../data/twitter_data_skipgram -minCount 10 -epoch 50 -neg 100"))
    subprocess.call(shlex.split("./fasttext skipgram -input ../data/twitter_data_corpus/corpus -output ../data/twitter_data_skipgram -minCount 10 -epoch 10 -neg 100"))


def dumps_as_cropus(filedir="../data/twitter_data_tokenized"):
    dir = filedir
    if os.path.exists("../data/twitter_data_corpus/corpus"):
        raise FileExistsError("corpus file already exists")
        sys.exit()    
    for abthpath in os.listdir(dir):
        with open(dir + "/" + abthpath) as r,open("../data/twitter_data_corpus/corpus","a+") as w:
            w.write("\n".join([ " ".join(t) for t in json.load(r)]))



if __name__ == "__main__":
    to_fasttext()
    sys.exit()
    dumps_as_cropus()
    # tokenize
    dir = "../data/twitter_data"
    for abthpath in os.listdir(dir):
        with open(dir + "/" + abthpath) as f:        
            li =[json.loads(t["post"])["text"] for t in json.load(f)]
        if len(li) < 10:
            print(len(li))
            continue
        user_texts = PreprocessorTextTwitter(li)
        user_texts.run(
            user_texts.remove_rt(),
            user_texts.remove_reply(),
            user_texts.remove_user_at(),
            # aa.remove_emoji(),
            user_texts.remove_url(),
            user_texts.remove_tag(),
            user_texts.normalize(),
            user_texts.set_for_tokenize()
            )
        user_texts.dump_as_tokens(dir + "_tokenized/" + abthpath)
        del user_texts


