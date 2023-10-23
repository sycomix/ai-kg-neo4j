# -*- coding: utf-8 -*-
# coding=utf-8
"""
create_author : zhangcl
create_time   : 2018-08-29
program       : *_* string and unicode converter *_*

汉字处理的工具:

判断unicode是否是汉字，数字，英文，或者其他字符。

全角符号转半角符号。

"""
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class UnicodeConvertor:
    """
    问题一：
    将u'\u810f\u4e71'转换为'\u810f\u4e71'
 
    方法：
    s_unicode = u'\u810f\u4e71'
    s_str = s_unicode.encode('unicode-escape').decode('string_escape')
 
    问题二：
    将'\u810f\u4e71'转换为u'\u810f\u4e71'
    
    方法：s_str = '\u810f\u4e71'
          s_unicode = s_str.decode('unicode-escape')
    """
    def __init__(self):
        """
        initialize local variables.
        """

        self.result = {}


def stringToUnicode(s_str):
    return s_str.encode('unicode-escape')

def numToUnicode(f_id):
    if isinstance(f_id, unicode):
        return f_id

    id = int(f_id)
    return str(id).decode('utf-8')



def unicodeToString(s_unicode):
    pass

def is_chinese(uchar):

    """判断一个unicode是否是汉字"""
    s_unicode = stringToUnicode(uchar)
    return s_unicode >= u'\\u4e00' and s_unicode <= u'\\u9fa5'

def is_empty(uchar):
    return uchar in [u' ', u'　']

def is_number(uchar):
    """判断一个unicode是否是数字"""

    return False



def is_alphabet(uchar):
    """判断一个unicode是否是英文字母"""

    uchar = stringToUnicode(uchar)

    return (uchar >= u'\\u0041' and uchar <= u'\\u005a') or (
        uchar >= u'\\u0061' and uchar <= u'\\u007a'
    )


def is_other(uchar):
    """判断是否非汉字，数字和英文字符"""

    return not (is_chinese(uchar) or uchar.isalnum())


def B2Q(uchar):
    """半角转全角"""

    inside_code = ord(uchar)

    if inside_code < 0x0020 or inside_code > 0x7e:  # 不是半角字符就返回原来的字符

        return uchar

    if inside_code == 0x0020:  # 除了空格其他的全角半角的公式为:半角=全角-0xfee0

        inside_code = 0x3000

    else:

        inside_code += 0xfee0

    return unichr(inside_code)


def Q2B(uchar):
    """全角转半角"""

    inside_code = ord(uchar)

    if inside_code == 0x3000:

        inside_code = 0x0020

    else:

        inside_code -= 0xfee0

    return (
        uchar
        if inside_code < 0x0020 or inside_code > 0x7E
        else unichr(inside_code)
    )


def stringQ2B(ustring):
    """把字符串全角转半角"""

    return "".join([Q2B(uchar) for uchar in ustring])


def uniform(ustring):
    """格式化字符串，完成全角转半角，大写转小写的工作"""

    return stringQ2B(ustring).lower()


def string2List(ustring):
    """将ustring按照中文，字母，数字分开"""

    retList = []

    utmp = []

    for uchar in ustring:

        if is_other(uchar):

            if len(utmp) == 0:
                continue

            retList.append("".join(utmp))

            utmp = []

        else:

            utmp.append(uchar)

    if len(utmp) != 0:
        retList.append("".join(utmp))

    return retList


if __name__ == "__main__":

    # test Q2B and B2Q

    for i in range(0x0020, 0x007F):
        print Q2B(B2Q(unichr(i))), B2Q(unichr(i))

    # test uniform

    ustring = u'中国 人名ａ高频Ａ'

    ustring = uniform(ustring)

    ret = string2List(ustring)

    print ret