# -*- coding: utf-8 -*-
# coding=utf-8
"""
create_author : zhangcl
create_time   : 2018-11-05
program       : *_*  course exam question *_*
"""
import os
import sys
from tool.convertor import UnicodeConvertor
reload(sys)
sys.setdefaultencoding('utf-8')

def resetColumnValue():
    for col_name in column_head_list:
        column_head_dict[col_name] = -1

def setColumnValueIncrease():
    for index, col_name in enumerate(column_head_list):
        column_head_dict[col_name] = index

column_head_list = [
    '高校名称',
    '课程名称',
    '课程编号',
    '试题编号',
    '题目内容',
    '题型名称',
    '试题类别',
    '难度',
    '选项A',
    '选项B',
    '选项C',
    '选项D',
    '选项E',
    '答案',
    '标注知识点',
    '电脑自动标注知识点',
]
column_head_dict = {}
# key 为列名称，value为index，这里由于未知，所以写-1，读取数据时，会把该值填写
resetColumnValue()

def getGoodCorrelationData():
    return ['试题序号', '试题内容', '电脑标识知识点', '可信度', '老师判断', '标注', '老师标识知识点']

class Examquestion:
    """
    课程的试题
    """

    def __init__(self):
        """
        initialize local variables.
        """
        # 试题的基本信息
        self.code = None
        self.type = None
        self.category = None
        self.diff = None
        self.content = None
        self.optA = None
        self.optB = None
        self.optC = None
        self.optD = None
        self.optE = None
        self.answer = None
        self.knowledge_list = []

    def initByList(self, question_row):
        self.course_code = question_row[column_head_dict[u'课程编号']]
        self.code = question_row[column_head_dict[u'试题编号']]
        self.content = question_row[column_head_dict[u'题目内容']]
        self.type = question_row[column_head_dict[u'题型名称']]
        self.category = question_row[column_head_dict[u'试题类别']]
        self.diff = question_row[column_head_dict[u'难度']]
        self.optA = question_row[column_head_dict[u'选项A']]
        self.optB = question_row[column_head_dict[u'选项B']]
        self.optC = question_row[column_head_dict[u'选项C']]
        self.optD = question_row[column_head_dict[u'选项D']]
        self.optE = question_row[column_head_dict[u'选项E']]
        self.answer = question_row[column_head_dict[u'答案']].upper()

        # 其他属性
        knowledge = ''
        if column_head_dict[u'标注知识点'] >= 0:
            knowledge = str(question_row[column_head_dict[u'标注知识点']])
            knowledge = knowledge.replace('；', ';')
            kwg_list = knowledge.split(';')
            self.knowledge_list = self.knowledge_list + kwg_list

    def toList(self):
        """
        将对象转换成列表
        
        :return: 
        """
        return [
            '',
            '',
            self.course_code,
            self.code,
            self.content,
            self.type,
            self.category,
            self.diff,
            self.optA,
            self.optB,
            self.optC,
            self.optD,
            self.optE,
            self.answer,
            '',
            self.getKnowlegeDescription(),
        ]
    def getKnowlegeDescription(self):
        kwg_list = []
        for k in self.knowledge_list:
            if isinstance(k, str):
                if len(k) > 0:
                    kwg_list.append(k)

                else:
                    continue
            else:
                desc = k.toDescription()
                kwg_list.append(desc)
        return u';'.join(kwg_list)
    def getContentAndAnswer(self):
        answer_content = ''
        if str(self.answer).__contains__('A'):
            answer_content = f'{answer_content}, {str(self.optA)}'
        if str(self.answer).__contains__('B'):
            answer_content = f'{answer_content}, {str(self.optB)}'
        if str(self.answer).__contains__('C'):
            answer_content = f'{answer_content}, {str(self.optC)}'
        if str(self.answer).__contains__('D'):
            answer_content = f'{answer_content}, {str(self.optD)}'
        if str(self.answer).__contains__('E'):
            answer_content = f'{answer_content}, {str(self.optE)}'
        answer_content = answer_content
        if len(answer_content) > 1:
            answer_content = answer_content[1:]
        content = f'{self.getKnowlegeDescription()} :: {self.content} 答案：{answer_content}'

        return content

    def getOnlyContentAndAnswer(self):
        answer_content = ''
        if str(self.answer).__contains__('A'):
            answer_content = f'{answer_content}, {str(self.optA)}'
        if str(self.answer).__contains__('B'):
            answer_content = f'{answer_content}, {str(self.optB)}'
        if str(self.answer).__contains__('C'):
            answer_content = f'{answer_content}, {str(self.optC)}'
        if str(self.answer).__contains__('D'):
            answer_content = f'{answer_content}, {str(self.optD)}'
        if str(self.answer).__contains__('E'):
            answer_content = f'{answer_content}, {str(self.optE)}'
        answer_content = answer_content
        if len(answer_content) > 1:
            answer_content = answer_content[1:]
        content = f'{self.content} 答案：{answer_content}'

        return content

class ExamquestionDictionary:
    """
    试题的集合
    """
    def __init__(self):
        """
        initialize local variables.
        """
        # key=school.code + course.code
        # 试题的key = course obj
        self.examquestion_dict = {}

        self.course_info = None

    def initByRows(self, rows):
        for row in rows:
            course_code = row[column_head_dict[u'课程编号']]
            course_code = UnicodeConvertor.numToUnicode(course_code)
            course = self.course_info.getCourseByCourseCode(course_code)
            self.__initByData(course, row)

    def __initByData(self, course, row):
        exam = Examquestion()
        exam.initByList(row)
        if self.examquestion_dict.__contains__(course):
            row_list = self.examquestion_dict.get(course)
            row_list.append(exam)
        else:
            row_list = [exam]
            self.examquestion_dict[course] = row_list
            #key = '{}-{}'.format(course.SchoolCode, course.CourseCode)
