from __future__ import unicode_literals
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import time

logging.basicConfig(
    format='%(asctime)s[%(levelname)s]%(message)s - File "%(name)s", function "%(method)s()"',
    level=logging.DEBUG,
    datefmt='%Y-%m-%d %H:%M:%S')

# logger = logging.getLogger("")

def clslog(logger):
    def log(cls):
        def deco_method(func):
            def inner(self, *args, **kwargs):
                logger.info("START",extra={"method":cls.__name__ + "." + func.__name__})
                result = func(self, *args, **kwargs)
                logger.info("FINISH",extra={"method":cls.__name__ + "." + func.__name__})
                return result
            return inner    
        for name, method in cls.__dict__.items():
            if not name.startswith('_'):
                setattr(cls, name, deco_method(method))
        return cls
    return log

    


    



