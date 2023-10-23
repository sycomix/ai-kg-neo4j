# -*- coding: utf-8 -*-
# coding=utf-8
"""
create_author : zhangcl
create_time   : 2018-11-05
program       : *_*  course exam question *_*
"""

class ResultInfo(object):
    def __init__(self, index, score, code, text):
        self.id = index
        self.code = code
        self.score = score
        self.text = text

    def toDescription(self):
        return f'{self.text}(可信度:{round(self.score * 100, 2)}%)'

    def toFullDescription(self):
        return f'{self.text}(编码：{self.code}，可信度:{round(self.score * 100, 2)}%)'