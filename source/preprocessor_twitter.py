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
# from collections import namedtuple
import queue
from preprocessor_base import TextPreprocessor
from preprocessor_log import clslog
from logging import getLogger

logger = getLogger(os.path.abspath(__file__))

@clslog(logger)
class PreprocessorTextTwitter(TextPreprocessor):
    def __init__(self,resource_dir,Project_name="twitter_sample"):
        super().__init__("twitter",resource_dir,Project_name)

    def user_to_vector_text(self):
        # for file_name in self.files:
        #     print(file_name + " processing to token...")
        #     with open(file_name) as f:
        #         result = []
        #         for post in json.load(f):
        #             result = result + self._process_text(json.loads(post["post"])["text"])
        #         with open(self.project_dirs_path["tokenized"] + "/" + os.path.splitext(os.path.basename(file_name))[0] + ".json","w") as w:
        #             json.dump(result,w,indent=4,ensure_ascii=False)
        self._process_token()

    def _process_text(self,text):
        result = self.text_processor.set(text).normalize().remove_emoji().remove_url().remove(
            "tag",
            "reply",
            "rt",
            "user_at"
        ).mecab()
        return result
    
    def _process_token(self):
        for process in self.processes["token"]:
            getattr(self.token_processor,process)(self.project_dirs_path["tokenized"],self.project_dirs_path[process])
           
if __name__ == "__main__":
    text = PreprocessorTextTwitter("./twitter_data","twitter_sample2")
    text.user_to_vector_text()