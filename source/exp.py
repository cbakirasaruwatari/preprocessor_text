from __future__ import unicode_literals
#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-
import re

class Exp:
    URL_PATTERN=re.compile(r"http\S+")


class ExpTwitter(Exp):
    RT_PATTERN=re.compile(r"(^(?:RT\s@.+:\s))",flags=re.MULTILINE | re.DOTALL)
    RT_INFORMAL_PATTERN=re.compile(r"(^(?:RT\s@.+:\s))",flags=re.MULTILINE | re.DOTALL)
    TAG_PATTERN=re.compile(r"(#[^\s]+)",flags=re.MULTILINE | re.DOTALL)
    REPLY_PATTERN=re.compile(r"^@([A-Za-z0-9_]+) ",flags=re.MULTILINE | re.DOTALL)
    USER_AT_PATTERN=re.compile(r"@([A-Za-z0-9_]+)",flags=re.MULTILINE | re.DOTALL)
