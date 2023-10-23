# -*- coding: utf-8 -*-
# coding=utf-8
"""
create_author : zhangcl
create_time   : 2018-11-12
program       : *_* read text data  *_*

"""
import sys
from domain import FilePath
reload(sys)
sys.setdefaultencoding('utf-8')

class TextReader:
    """
    read data from word file.
    """

    def __init__(self):
        """
        initialize data
        """
        self.filepath = None
        self.content_rows = None

    def readText(self):
        self.content_rows = []
        if self.filepath is None:
            return
        if not FilePath.fileExist(self.filepath):
            return

        f_input = open(self.filepath)
        self.content_rows.extend(iter(f_input))
        return self.content_rows