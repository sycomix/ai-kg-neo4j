# -*- coding: utf-8 -*-
# coding=utf-8
"""
create_author : zhangcl
create_time   : 2018-10-11
program       : *_*  define course information *_*
"""
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import FilePath

class CourseBase:
    """
    基础课程
    """
    coursebase_index = 0
    coursebase_code = None
    coursebase_name = None

    def initByString(self, data):
        items = data.split(' ')
        self.coursebase_code = items[0]
        self.coursebase_name = items[1]

        items = self.coursebase_code.split('.')
        self.coursebase_index = int(items[-1])


class Course(CourseBase):
    """
    course information.
    """

    def __init__(self):
        """
        initialize local variables.
        """
        self.prefix = 'SchoolCode,SchoolName,CourseCode,OldCourseName,ItemBankID,CourseID,NewCourseName,AppID,CreateOrgID,'
        self.SchoolCode = None
        self.SchoolName = None
        self.CourseCode = None
        self.OldCourseName = None
        self.ItemBankID = None
        self.CourseID = None
        self.NewCourseName = None
        self.AppID = None
        self.CreateOrgID = None

    def toString(self):
        item_list = [
            self.SchoolName,
            self.SchoolCode,
            self.NewCourseName,
            self.CourseCode,
            self.ItemBankID,
        ]
        return ','.join(item_list)

    def toStringByColumns(self):
        """
        'SchoolCode,SchoolName,CourseCode,OldCourseName,ItemBankID,CourseID,NewCourseName,AppID,CreateOrgID,'
        :return: 
        """
        item_list = [
            self.SchoolCode,
            self.SchoolName,
            self.CourseCode,
            self.OldCourseName,
            self.ItemBankID,
            self.CourseID,
            self.NewCourseName,
            self.AppID,
            self.CreateOrgID,
            self.coursebase_name,
            self.coursebase_code,
        ]
        return self.prefix + ','.join(item_list)

class CourseScore:
    """
    课程与试题的得分统计信息
    
    """
    def __init__(self):
        """
        initialize local variables.
        """
        self.course = None
        self.school_code = None
        self.school_name = None
        self.course_code = None
        self.course_name = None

        self.score_scope_more60_count = 0
        self.score_scope_between5060_count = 0
        self.score_scope_between4050_count = 0
        self.score_scope_less40_count = 0

        self.score_scope_total = 0

        self.score_scope_more60_rate = 0.0
        self.score_scope_between5060_rate = 0.0
        self.score_scope_between4050_rate = 0.0
        self.score_scope_less40_rate = 0.0

    def toString(self):
        """
        将对象以字符串输出
        properties = []
        :return: 
        """
        properties = [
            self.school_code,
            self.school_name,
            self.course_code,
            self.course_name,
            str(self.score_scope_more60_count),
            str(self.score_scope_between5060_count),
            str(self.score_scope_between4050_count),
            str(self.score_scope_less40_count),
            str(self.score_scope_more60_rate),
            str(self.score_scope_between5060_rate),
            str(self.score_scope_between4050_rate),
            str(self.score_scope_less40_rate),
        ]
        return ','.join(properties)

    def initByString(self, course_str):
        """
        从tostring的结果解析出来
        :param course_str: 
        :return: 
        """
        if len(course_str) == 0:
            return
        properties = course_str.split(',')
        if len(properties) < 12:
            return

        self.school_code = properties[0]
        self.school_name = properties[1]
        self.course_code = properties[2]
        self.course_name = properties[3]

        self.score_scope_more60_count = int(properties[4])
        self.score_scope_between5060_count = int(properties[5])
        self.score_scope_between4050_count = int(properties[6])
        self.score_scope_less40_count = int(properties[7])

        self.score_scope_more60_rate = float(properties[8])
        self.score_scope_between5060_rate = float(properties[9])
        self.score_scope_between4050_rate = float(properties[10])
        self.score_scope_less40_rate = float(properties[11])

    def initCourse(self,course):
        """
        初始化课程信息
        
        :param course: 
        :return: 
        """
        self.course = course
        self.school_code = course.SchoolCode
        self.school_name = course.SchoolName
        self.course_code = course.CourseCode
        self.course_name = course.NewCourseName

    def compute(self):
        """
        计算总数和比率
        :return: 
        """
        self.score_scope_total = self.score_scope_more60_count + self.score_scope_between5060_count
        self.score_scope_total += self.score_scope_between4050_count + self.score_scope_less40_count
        if self.score_scope_total == 0:
            return
        self.score_scope_more60_rate = float(self.score_scope_more60_count) / self.score_scope_total
        self.score_scope_between5060_rate = float(self.score_scope_between5060_count) / self.score_scope_total
        self.score_scope_between4050_rate = float(self.score_scope_between4050_count) / self.score_scope_total
        self.score_scope_less40_rate = float(self.score_scope_less40_count) / self.score_scope_total

    def getDescription(self):
        result_list = []
        if self.course is not None or (self.school_name is not None):
            ns = f'院校信息：{self.school_name}  {self.school_code}'
            result_list.append(ns)

            ns = f'课程信息：{self.course_name}  {self.course_code}'
            result_list.append(ns)

        self.compute()
        ns = f'试题总数：{self.score_scope_total}'
        result_list.append(ns)

        ns = f'比较靠谱数(60分以上)：{self.score_scope_more60_count}  ，比较靠谱占比：{round(self.score_scope_more60_rate * 100, 2)}%'
        result_list.append(ns)

        ns = f'基本靠谱数(50-60分)：{self.score_scope_between5060_count}  ，基本靠谱占比：{round(self.score_scope_between5060_rate * 100, 2)}%'
        result_list.append(ns)

        ns = f'不太靠谱数(40-50分)：{self.score_scope_between4050_count}  ，不太靠谱占比：{round(self.score_scope_between4050_rate * 100, 2)}%'
        result_list.append(ns)

        ns = f'不靠谱数(40分以下)：{self.score_scope_less40_count}  ，不靠谱占比：{round(self.score_scope_less40_rate * 100, 2)}%'
        result_list.append(ns)

        return result_list

class CourseFilepath:
    """
    课程文件的位置, 根据给定源文件的路径，然后在该目录下生成相关的文件路径，并保持结果
    可以指定源文件类型，根据不同类型解析出txt格式，
    """

    def __init__(self):
        self.__curpath = os.path.dirname(os.path.realpath(__file__))
        self.course = None
        # 源文件的文件类型
        self.type_docx = u'docx'
        self.type_text = u'txt'
        self.sourse_filetype = self.type_docx
        # 课程课件源文件的文件路径，分不同的文件类别
        self.courseware_source_directory = None
        self.courseware_source_pdf_filepath = None
        self.courseware_source_doc_filepath = None
        self.courseware_source_docx_filepath = None
        # 从以上格式中抽取出来的文本结果文件路径
        self.courseware_source_txt_filepath = None
        # 从课程课件的txt文件中抽取出来的知识点结果文件路径
        self.courseware_knowledge_txt_filepath = None
        # 课程题库源文件的文件路径
        self.examquestion_source_xlsx_filepath = None
        # 从上面的excel文件中生成的txt文件，分析和作为训练模型的语料
        self.examquestion_source_txt_filepath = None

        # 训练使用的语料文件路径，是由上面3个txt文件的合成语料
        self.vector_corpus_txt_filepath = None
        self.vector_model_bin_filepath = None

        # 知识点和问题的关联文件
        self.correlation_txt_filepath = None
        # 关联差的试题
        self.correlation_bad_xls_filepath = None
        # 关联的cypher语句
        self.cypher_txt_filepath = None
        # 关联后的好的结果
        self.correlation_good_xls_filepath = None

        #self.__initByCourse(course)

    def initByCourse(self, course, source_filetype=None):
        """
        通过课程对象信息，来创建文件路径的生成
        :param course: 
        :param source_filetype:
        :return: 
        """
        if source_filetype is not None:
            self.sourse_filetype = source_filetype

        self.course = course
        full_filename = f'{course.SchoolName}-{course.SchoolCode}-{course.NewCourseName}-{course.CourseCode}'
        filename = f'{course.SchoolCode}-{course.CourseCode}'
        coursebase_filename = f'{course.coursebase_name}-{course.coursebase_code}'
        # 生成转换c-src-txt的文件夹，该文件夹内的内容为文本文件结构，内容与源文件一致
        FilePath.mkdir(f'{self.courseware_source_directory}/c-src-txt')
        self.courseware_source_txt_filepath = (
            f'{self.courseware_source_directory}/c-src-txt/{filename}.txt'
        )

        # 生成转换c-kwg-txt的文件夹，该文件夹内的内容为文本文件结构，内容为抽取的知识点
        FilePath.mkdir(f'{self.courseware_source_directory}/c-kwg-txt')
        self.courseware_knowledge_txt_filepath = f'{self.courseware_source_directory}/c-kwg-txt/{coursebase_filename}.txt'

        # 生成转换q-src-txt的文件夹，该文件夹内的内容为文本文件结构，内容为试题的文本文件
        FilePath.mkdir(f'{self.courseware_source_directory}/q-src-xls')
        self.examquestion_source_xlsx_filepath = (
            f'{self.courseware_source_directory}/q-src-xls/{filename}.xls'
        )

        # 生成转换q-src-txt的文件夹，该文件夹内的内容为文本文件结构，内容为试题的文本文件
        FilePath.mkdir(f'{self.courseware_source_directory}/q-src-txt')
        self.examquestion_source_txt_filepath = (
            f'{self.courseware_source_directory}/q-src-txt/{filename}.txt'
        )


        # 生成上面3个txt文件，分词后合成的语料文件，corpus-txt的文件夹
        FilePath.mkdir(f'{self.courseware_source_directory}/corpus-txt')
        self.vector_corpus_txt_filepath = f'{self.courseware_source_directory}/corpus-txt/{coursebase_filename}.txt'

        # 生成模型文件夹，model-bin
        FilePath.mkdir(f'{self.courseware_source_directory}/model-bin')
        self.vector_model_bin_filepath = f'{self.courseware_source_directory}/model-bin/{coursebase_filename}.model.bin'

        # 生成关联后的文本文件，k-q-txt文件夹
        FilePath.mkdir(f'{self.courseware_source_directory}/k-q-txt')
        self.correlation_txt_filepath = (
            f'{self.courseware_source_directory}/k-q-txt/{coursebase_filename}.txt'
        )

        # 生成关联后结果较差的excle文件，k-q-bad-xls文件夹
        FilePath.mkdir(f'{self.courseware_source_directory}/k-q-bad-xls')
        self.correlation_bad_xls_filepath = f'{self.courseware_source_directory}/k-q-bad-xls/{coursebase_filename}.xls'
        FilePath.mkdir(f'{self.courseware_source_directory}/k-q-good-xls')
        self.correlation_good_xls_filepath = f'{self.courseware_source_directory}/k-q-good-xls/{coursebase_filename}.xls'
        # 生成关联后的文本文件，cypher-txt文件夹，用于导入到图数据库
        FilePath.mkdir(f'{self.courseware_source_directory}/cypher-txt')
        self.cypher_txt_filepath = (
            f'{self.courseware_source_directory}/cypher-txt/{coursebase_filename}'
        )



class CourseDictionary:
    """
    course information dict.
    """

    def __init__(self, course_source_filename):
        """
        initialize local variables.
        """
        self.__curpath = os.path.dirname(os.path.realpath(__file__))


        self.course_code_dict = {}
        self.course_id_dict = {}
        self.course_name_dict = {}
        self.course_school_name_dict = {}

        #self.__filepath = '{}/../data/dictionary/course-20181026.txt'.format(self.__curpath)
        self.__filepath = (
            f'{self.__curpath}/../data/dictionary/{course_source_filename}'
        )
        self.initDictionary(self.__filepath)

    def initDictionary(self, filepath=None):

        if len(self.course_code_dict.keys()) > 0:
            return
        if self.__filepath is None and filepath is None:
            return
        else:
            filepath = self.__filepath
        if not FilePath.fileExist(filepath):
            return

        for n_course in self.readOneCourseOnce(filepath):
            self.course_code_dict[n_course.CourseCode] = n_course
            self.course_id_dict[n_course.CourseID] = n_course
            self.course_name_dict[n_course.NewCourseName] = n_course
            self.course_school_name_dict[n_course.SchoolName+n_course.NewCourseName] = n_course


    def readOneCourseOnce(self, filepath):
        with open(filepath, 'r') as f:
            for line in f:
                # 用逗号分隔
                item_array = line.split(u',')
                length_item = len(item_array)
                if length_item < 18:
                    continue
                n_course = Course()
                n_course.SchoolCode = item_array[9].strip()
                n_course.SchoolName = item_array[10].strip()
                n_course.CourseCode = item_array[11].strip()
                n_course.OldCourseName = item_array[12].strip()
                n_course.ItemBankID = item_array[13].strip().upper()
                n_course.CourseID = item_array[14].strip().upper()
                n_course.NewCourseName = item_array[15].strip()
                n_course.AppID = item_array[16].strip().upper()
                n_course.CreateOrgID = item_array[17].strip().upper()
                if length_item == 20:
                    n_course.coursebase_name = item_array[18].strip()
                    n_course.coursebase_code = item_array[19].strip()

                yield n_course


    def getBankIdByCourseCode(self, coursecode):
        bankid = None
        str_id = str(coursecode)
        if self.course_code_dict.__contains__(str_id):
            course = self.course_code_dict[str_id]
            bankid = course.ItemBankID

        return bankid

    def getCourseByCourseCode(self, coursecode):
        return (
            self.course_code_dict[coursecode]
            if self.course_code_dict.__contains__(coursecode)
            else None
        )

    def getCourseByCourseId(self, courseid):
        return (
            self.course_id_dict[courseid]
            if self.course_id_dict.__contains__(courseid)
            else None
        )

    def getCourseByCoursename(self, name):
        course = None
        str_id = str(name)
        if self.course_name_dict.__contains__(str_id):
            course = self.course_name_dict[str_id]
        else:
            course = Course()
            course.NewCourseName = name
            course.CourseCode = 'default'
            course.SchoolName = ''
        return course

    def getCourseBySchoolAndCoursename(self, name):
        course = None
        if self.course_school_name_dict.__contains__(name):
            course = self.course_school_name_dict[name]
        else:
            course = Course()
            course.NewCourseName = name
            course.CourseCode = 'default'
            course.SchoolName = ''
        return course

if __name__ == "__main__":
    pusher = CourseDictionary()
    filepath = u'D:/奥鹏/course.txt'
    pusher.initDictionary(filepath)
    print 'over'