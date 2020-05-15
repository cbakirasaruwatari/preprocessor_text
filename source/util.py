#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import json
import os
import configparser
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

def config(path):
    if os.path.isfile(path) is False:
        raise FileNotFoundError("設定ファイルがないよ")
    cfg = configparser.ConfigParser(os.environ)
    cfg.read(path)

    return cfg

def flatten(li):
    return list(itertools.chain.from_iterable(li))


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