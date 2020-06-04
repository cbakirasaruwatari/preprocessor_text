from __future__ import unicode_literals
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import pathlib
import json
from abc import ABCMeta, abstractmethod
import re
from typing import Callable
from dataclasses import dataclass
from collections import deque
import textprocess
import tokenprocess
from util import getter,setter,load_yaml

class PreprocessorBase(metaclass=ABCMeta):
    @dataclass(frozen=True)
    class Settings:
        pj_name: str
        resource_path: pathlib.Path
        kind: str
        domain: str
        processes: dict
        def __post_init__(self):
            self._validate()
        def _validate(self):
            # TODO processes field must be validated.
            if self.kind not in (kind_supported := ["text"]):
                raise NotImplementedError("kind field must be " + str(kind_supported))
            elif self.domain not in (domain_supported := ["twitter"]):
                raise NotImplementedError("domain field must be " + str(domain_supported))

    class Procedure:
        def __init__(self,settings,func):
            self.task:dict = settings.processes
            self.validate_func: Callable = func
            self._validate()
        def _validate(self):
            self.validate_func(self.task)

    class Project:
        def __init__(self,settings):
            self.name:str = settings.pj_name
            self.processes:dict = settings.processes
            self.resource_path:pathlib.Path = settings.resource_path
            self.destination_path:dict
            self._create()

        def _create(self):
            dirs = {}
            for v in ["/others","/result"]:
                # os.makedirs(pathlib.Path(self.name +v))
                dirs[v[1:]] = pathlib.Path(self.name +v).resolve()

            for k,v in self.processes.items():
                if type(v) == str:
                    dirs[k + "_" + v] = self._create_dir(k,v)
                else:
                    for v2 in v:
                        dirs[k + "_" + v2] = self._create_dir(k,v2)
            self.destination_path = dirs
            print(self.destination_path)
        
        def _create_dir(self,k,v):
            dir = pathlib.Path(self.name + "/" + k + "process" + "/" + v)
            # os.makedirs(dir)
            return dir.resolve()
            

    def __init__(self,setting_path):
        self.setting_path = setting_path
        yaml = load_yaml(setting_path)
        self.settings = self.Settings(
            yaml["project"]["name"],
            pathlib.Path(yaml["project"]["resource_path"]).resolve(),
            yaml["project"]["kind"],
            yaml["project"]["domain"],
            yaml["project"]["processes"])
        self.project = self.Project(self.settings)
        self.procedure = self.Procedure(self.settings,self._validate_processes)    
        
    @abstractmethod
    def _validate_processes(self,task):
       raise  NotImplementedError
        
class TextPreprocessor(PreprocessorBase,metaclass=ABCMeta):
    def __init__(self,module_name,setting_path):
        self.text_processor = getattr(textprocess,"TextProcess"+module_name.capitalize())(module_name)
        self.token_processor = tokenprocess.TokenProcess()
        super().__init__(setting_path)
    
    def _validate_processes(self,task):
        # TODO 実装
        print(task)

    @abstractmethod
    def _process_token(self):
        raise NotImplementedError
    @abstractmethod
    def _process_text(self):
        raise NotImplementedError