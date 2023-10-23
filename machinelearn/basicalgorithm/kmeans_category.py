# -*- coding: utf-8 -*-
# coding=utf-8
"""
create_author : zhangcl
create_time   : 2018-11-14
program       : *_*  kmeans cluster information *_*
"""
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import numpy as np
from gensim.models import KeyedVectors
from gensim.models.word2vec import LineSentence, Word2Vec
from domain import FilePath, CourseInfomation, ResultInfo
from tool.processor import SentenceProcessor
from tool.reader import SentenceReader

class KmeansCategory:
    """
        catalog information.
        """

    def __init__(self, course_path_info):
        """
        initialize local variables.
        """
        self.model_loaded = None
        # 定义分词器
        self.sentence_reader = SentenceReader.SentenceReader()
        self.sentence_processor = SentenceProcessor.SenPreprocess()

        # 训练样本文件路径信息，中间结果信息，模型结果信息等
        self.course_path_info = course_path_info

        # 课程名称列表
        self.course_name_list = None

        # 字符串与分词后的对应map
        self.sentence_words_dict = {}

        # 分类目录数据
        self.catalog_code_dict = {}
        # 课程与分类的结果
        self.course_catalogs_good_dict = {}
        self.course_catalogs_bad_dict = {}

        # 未识别的课程归属类别
        self.course_catalog_unknow_list = []

        self.stopwords = [u'学', u'类', u'中国', u'国际', u'国外', u'西方']

        # 获取第二层的分类
        self.snd_level_catalog = []

    def generate_train_file(self):
        self.sentence_words_dict = {}
        with open(self.course_path_info.vector_corpus_txt_filepath, 'w') as f_out:
            # 第二步抽取的课程列表也作为训练样本
            if self.course_name_list:
                for course_name in self.course_name_list:
                    course_name1 = self.preprocessSent(course_name)
                    # word_list = self.sentence_reader.hanlpsplitor.extractKeyword(course_name, 1)
                    word_list = self.sentence_reader.splitSentenceCanRepeat(course_name1)
                    word_list = self.postWordList(word_list)
                    f_out.write(' '.join(word_list))
                    f_out.write('\n')

                    self.sentence_words_dict[course_name] = word_list

    def train(self):

        # 先检查模型是否存在，如果存在，直接加载
        if FilePath.fileExist(self.course_path_info.vector_model_bin_filepath):
            # self.model_loaded = Word2Vec.load_word2vec_format(self.model_file, binary=True)
            self.model_loaded = KeyedVectors.load_word2vec_format(self.course_path_info.vector_model_bin_filepath,
                                                                  binary=True)
            # 输出词典
            # self.output_dict(self.model_loaded.wv.index2word)
            # 生成语料
            self.generate_train_file()
            return

        # 生成语料
        self.generate_train_file()

        # 加载语料
        # sentences = word2vec.Text8Corpus(self.train_output_result_file)
        sentences = LineSentence(self.course_path_info.vector_corpus_txt_filepath)
        # 训练skip-gram模型，默认window=5
        # 第一个参数是训练语料，第二个参数是小于该数的单词会被剔除，默认值为5, 第三个参数是神经网络的隐藏层单元数，默认为100
        # 注意：min_count = 1,就是所有词，如果设置大的话，会过滤掉小于的词
        print '正在训练模型...'
        model = Word2Vec(sentences, size=500, min_count=1, iter=1000)
        # model.wv.save(self.model_file)
        model.wv.save_word2vec_format(self.course_path_info.vector_model_bin_filepath, binary=True)

        self.model_loaded = model

    def getSentenceVector(self, words_list):
        arr = [self.model_loaded.wv[w] for w in words_list]
        np_array = np.array(arr)
        return np_array.mean(axis=0)

    def pred_similarity(self, question_words, knowledge_words):
        # 判断问题和知识点之间的向量相似度
        print 'question_words:' + ' '.join(question_words)
        print 'knowledge_words:' + ' '.join(knowledge_words)
        score = self.model_loaded.wv.n_similarity(question_words, knowledge_words)
        return score

    def predication(self):
        # 遍历每一个课程，选择相似度最高的分类（前三个）
        for course_name in self.course_name_list:
            if not self.sentence_words_dict.__contains__(course_name):
                continue

            course_name_word_list = self.sentence_words_dict[course_name]
            if len(course_name_word_list) == 0:
                self.course_catalog_unknow_list.append(course_name)
                continue
            res_list = []
            for index, catalog_name in enumerate(self.catalog_code_dict.keys()):
                catalog_tuple = self.catalog_code_dict.get(catalog_name)
                catalog_code = catalog_tuple[0]
                catalog_name_word_list = catalog_tuple[2]

                score = self.pred_similarity(course_name_word_list, catalog_name_word_list)
                res = ResultInfo.ResultInfo(index, score, catalog_code, catalog_name)
                res_list.append(res)
            # 对列表按score降序排列
            res_list.sort(cmp=None, key=lambda x: x.score, reverse=True)

            # 选前3个最高的得分分类
            best_candidate_list = res_list[:3]
            if best_candidate_list[0].score > 0.45:
                self.course_catalogs_good_dict[course_name] = best_candidate_list
            else:
                self.course_catalogs_bad_dict[course_name] = best_candidate_list

    def output_dict(self):
        filepath = self.course_path_info.correlation_txt_filepath
        with open(filepath, 'w') as fout:
                # 好的结果
            good_result_desc = f'好的结果：{len(self.course_catalogs_good_dict.keys())}'
            fout.write(good_result_desc)
            fout.write('\n')
            for course_name in self.course_catalogs_good_dict.keys():
                catalog_list = self.course_catalogs_good_dict.get(course_name)
                res_list = [
                    result_catalog.toFullDescription()
                    for result_catalog in catalog_list
                ]
                out_line = f"{course_name} -- {';'.join(res_list)}"
                fout.writelines(out_line)  # 将分词好的结果写入到输出文件
                fout.writelines('\n')

                # 不好的结果
            bad_result_desc = f'不好的结果：{len(self.course_catalogs_bad_dict.keys())}'
            fout.write('\n\n\n')
            fout.write(bad_result_desc)
            fout.write('\n')
            for course_name in self.course_catalogs_bad_dict.keys():
                catalog_list = self.course_catalogs_bad_dict.get(course_name)
                res_list = [
                    result_catalog.toFullDescription()
                    for result_catalog in catalog_list
                ]
                out_line = f"{course_name} -- {';'.join(res_list)}"
                fout.writelines(out_line)  # 将分词好的结果写入到输出文件
                fout.writelines('\n')

            # 输出未被识别的课程
            fout.writelines('\n\n')
            for course_name in self.course_catalog_unknow_list:
                fout.write(course_name)
                fout.writelines('\n')

    def readCourseNameList(self):
        """
        批量处理多个课程的名字提取
        :return: 
        """
        self.course_name_list = []
        # 指定一个文件夹，该文件夹用来存放多个课程的pdf课件
        # 逐个课件处理
        # 首先指定根目录位置
        srcrootpath = u'./../../data/course-knowledge-machine/20181026-600plus/c-docx'
        # os.walk(path)这个函数得到的结果是一个或多个tuple，
        # 或者使用os.listdir(path)函数能得到文件夹下所有文件（包括文件夹）的名称，但是无法获取子文件夹的状态
        count = 0
        filelist = self.get_filename_from_dir(srcrootpath)
        # 然后是对每一个文件进行处理
        for f in filelist:
            count = count + 1
            self.coursename = os.path.splitext(f)[0]

            # 判断该课程是否在需要处理的范围之内，如果不是，则跳过该课程
            current_coursename = self.getCourseNameFromFileName(self.coursename)
            # current_schoolname = self.getSchoolNameFromFileName(self.coursename)

            self.course_name_list.append(current_coursename)
            print '第{0}篇 课程：{1} 处理完成；'.format(count, f)

        print '所有课程处理完毕，共处理：{0}篇'.format(count)

    def get_filename_from_dir(self, dir_path):
        file_list = []
        if not os.path.exists(dir_path):
            return file_list

        for item in os.listdir(dir_path):
            basename = os.path.basename(item)
            # print(chardet.detect(basename))   # 找出文件名编码,文件名包含有中文

            # windows下文件编码为GB2312，linux下为utf-8
            try:
                decode_str = basename.decode("GB2312")
            except UnicodeDecodeError:
                decode_str = basename.decode("utf-8")

            if decode_str.startswith(u'~'):
                continue

            file_list.append(decode_str)

        return file_list

    def getCourseNameFromFileName(self, filename):
        """
        从文件名称中，获取到课程名称，文件名称为：福师《外国法制史》.docx
        从文件名称抽取出课程名称，这里抽取出中括号内的名称：外国法制史
        :param filename: 
        :return: 
        """
        course_list = self.sentence_processor.find_VIP_words_by_pattern(filename)
        course_name = ''
        if len(course_list) > 0:
            course_name = course_list[0]
            course_name = str(course_name).replace(u'（', u'(')
            course_name = course_name.replace(u'）', u')')
        return course_name

    def preprocessSent(self, sent):
        """
        预处理，比如处理最后是学字
        :param sent: 
        :return: 
        """
        if isinstance(sent, str):
            sent = sent.decode('utf-8')

        # 去掉，学，类，中国，国外，国际等对分类，干扰的词汇
        for stopword in self.stopwords:
            if sent.__contains__(stopword):
                sent = sent.replace(stopword, u' ')

        return sent

    def postWordList(self, word_list):

        result_list = []
        for word in word_list:
            if word == u'学':
                continue
            if word.startswith(u'概'):
                continue

            result_list.append(word)

        return result_list

    def outfile(self, filepath):
        with open(filepath, 'w') as fout:
            fout.writelines(self.snd_level_catalog)


if __name__ == "__main__":

    course_path_info = CourseInfomation.CourseFilepath()
    course_path_info.courseware_source_txt_filepath = u'./../../data/course-base/本科专业目录-catalog.xlsx.txt'
    course_path_info.vector_corpus_txt_filepath = u'./../../data/course-base/本科专业目录-catalog.corpus.txt'
    course_path_info.vector_model_bin_filepath = u'./../../data/course-base/本科专业目录-catalog.model.bin'
    course_path_info.correlation_txt_filepath = u'./../../data/course-base/本科专业目录-course-catalog.txt'
    sr = KmeansCategory(course_path_info)
    #sr.course_path_info = course_path_info

    sr.readCourseNameList()
    sr.train()
    sr.predication()
    sr.output_dict()
    filepath = u'./../../data/course-base/本科专业目录-course-catalog-tag.txt'
    sr.outfile(filepath)
