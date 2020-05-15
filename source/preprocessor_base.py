from __future__ import unicode_literals
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import random
import pathlib
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
# from collections import namedtuple
import queue
import textprocess
import tokenprocess
from abc import ABCMeta, abstractmethod


class PreprocessorBase(metaclass=ABCMeta):
    def __init__(self,resource_dir,project_name,processes):
        self.resource_dir = resource_dir
        self.files = [resource_dir + "/" + f for f in os.listdir(resource_dir) if os.path.isfile(os.path.join(resource_dir, f))]
        self.project_name = project_name
        self.project = Project(project_name,processes)
        self.project_dirs_path = self.project.create()

    
class Project(object):
    def __init__(self,name,dirs):
        self.project_name = name
        self.project_dirs = dirs
        
    def create(self):
        project_dirs_path = {}
        project_dirs_path["tokenized"] = "./" + self.project_name + "/" + self.project_dirs["text"]
        for dir in ["./" + self.project_name,"./" + self.project_name + "/row","./" + self.project_name + "/" + self.project_dirs["text"]]:
            pass
            os.mkdir("./" + dir)
        for dir in self.project_dirs["token"]:
            os.mkdir("./" + self.project_name + "/" + dir)
            project_dirs_path[dir] = "./" + self.project_name + "/" + dir
        return project_dirs_path
        
class TextPreprocessor(PreprocessorBase,metaclass=ABCMeta):
    def __init__(self,module_name,resource_dir,project_name):
        self.text_processor = getattr(textprocess,"TextProcess"+module_name.capitalize())(module_name)
        self.token_processor = tokenprocess.TokenProcess()
        # self.processes = ["tokenize","row","corpus","frequency","tfidf","skipgram"]
        self.processes = {"text":"mecab","token":["tokenize","row","corpus","frequency","skipgram"]}
        super().__init__(resource_dir,project_name,self.processes)
    
    # @abstractmethod
    # def run(self):
    #     raise NotImplementedError
    @abstractmethod
    def _process_token(self):
        raise NotImplementedError
    @abstractmethod
    def _process_text(self):
        raise NotImplementedError