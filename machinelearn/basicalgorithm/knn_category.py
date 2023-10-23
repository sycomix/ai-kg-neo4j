# -*- coding: utf-8 -*-
# coding=utf-8
"""
create_author : zhangcl
create_time   : 2018-11-14
program       : *_*  save knowledge information *_*
"""
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from tool.httprequest import HttpRequester

class KnnCategory:
    """
        catalog information.
        """

    def __init__(self):
        """
        initialize local variables.
        """
        # 设置源文件，中间文件，结果文件的路径
        self.course_path_info = None

    def generate_train_file(self):

        with open(self.course_path_info.vector_corpus_txt_filepath, 'w') as f_out:
            # 第一步先加载分类目录
            if self.course_path_info.courseware_source_txt_filepath:
                for c_line in self.sentence_reader.splitSentence(self.course_path_info.courseware_source_txt_filepath):
                    f_out.write(' '.join(c_line))
                    f_out.write('\n')
