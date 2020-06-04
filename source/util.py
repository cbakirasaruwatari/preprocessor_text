#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import json
import os
import configparser
import yaml
import itertools

def _getprop(func):
    return sys._getframe(2).f_locals.get(func.__name__, None)

def getter(func):
    prop = _getprop(func)
    if prop is None:
        return property(func)
    return prop.getter(func)

def setter(func):
    prop = _getprop(func)
    if prop is None:
        return property(None, func)
    return prop.setter(func)

def deleter(func):
    prop = _getprop(func)
    if prop is None: 
        return property(None, None, func)
    return prop.setter(func)

# def config(path):
#     if os.path.isfile(path) is False:
#         raise FileNotFoundError("設定ファイルがないよ")
#     cfg = configparser.ConfigParser(os.environ)
#     cfg.read(path)

    # return cfg

def flatten(li):
    return list(itertools.chain.from_iterable(li))

def exception_handler(func,is_return=False,exp=Exception, handle=lambda x : x, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except exp as e:
        if is_return:
            return(e)
        else:
            pass

def load_json(path):
    with open(path) as r:
      result = json.load(r)
    return result

def load_yaml(path):
    with open(path) as r:
        return yaml.load(r, Loader=yaml.SafeLoader)


# def log_info_cls(cls):
#     def deco_method(func):
#         def inner(self, *args, **kwargs):
#             logger.info("start",extra={"method":cls.__name__ + "." + func.__name__})
#             result = func(self, *args, **kwargs)
#             return result
#         return inner    
#     for name, method in cls.__dict__.items():
#         if not name.startswith('_'):
#             setattr(cls, name, deco_method(method))
#     return cls