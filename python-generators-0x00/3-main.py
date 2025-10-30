#!/usr/bin/python3
import sys
from lazy_paginate import lazy_pagination

try:
    for page in lazy_pagination(100):
        for user in page:
            print(user)
except BrokenPipeError:
    sys.stderr.close()
