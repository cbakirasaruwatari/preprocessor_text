from __future__ import unicode_literals
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import functools
import re
import json
import sys
# import subprocess
# import shlex
# import itertools
# from collections import Counter
# from dataclasses import dataclass,asdict
# from util import getter,setter,config,flatten
from typing import Optional,Union,NewType,Tuple, List, Any, Dict, Callable, Generic, NoReturn

import MeCab
import emoji
import neologdn

from util import setter,getter
import exp

class TextProcess():
    MECAB_DICT_PATH:str='/usr/local/lib/mecab/dic/mecab-ipadic-neologd'
    text:str=None

    def __init__(self,name):
        self.exp = getattr(exp,"Exp"+name.capitalize())()

    def set(self,text:str=None):
        self.text = text
        return self

    def get(self):
        return self.text
    
    def normalize(self):
        '''
        # see https://github.com/neologd/mecab-ipadic-neologd/wiki/Regexp.ja#python-written-by-hideaki-t--overlast
        '''
        self.set(neologdn.normalize(self.text))
        return self

    def remove_emoji(self):
        '''
        # All emoji must be deleted in the text.
        '''        
        self.set(''.join(c for c in self.text if c not in emoji.UNICODE_EMOJI))
        return self

    def remove_url(self):
        '''
        # All url must be deleted in the text.
        '''
        self.set(self.exp.URL_PATTERN.sub("",self.text))
        return self
    
    def mecab(self) -> list:
        '''
        # separated by mecab.
        '''
        self.text.replace("\n", " ")
        tokenizer = MeCab.Tagger ('-d ' + self.MECAB_DICT_PATH)
        tokenizer.parse('')
        node = tokenizer.parseToNode(self.text)
        keywords = ["<BOS>"]
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
        keywords.append("<EOS>")
        self.set()
        return keywords

class TextProcessTwitter(TextProcess):

    def remove(self,*keywords:str) -> str:
        for keyword in keywords:
            if not hasattr(self.exp,keyword.upper() + "_PATTERN"):
                raise AttributeError()
                sys.exit()
        for keyword in keywords:
            self.set(getattr(self.exp,keyword.upper() + "_PATTERN").sub("",self.text))
        return self

    def replace(self):
        pass