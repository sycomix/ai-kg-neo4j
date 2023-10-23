# -*- coding: utf-8 -*-
# coding=utf-8
"""
create_author : zhangcl
create_time   : 2018-07-16
program       : *_* word net generate *_*

"""

import sys

from database import Neo4jHandler
from tool.reader import SentenceReader
from tool.splitor import HanlpSplitor

reload(sys)
sys.setdefaultencoding('utf-8')
class WordnetGenerator:
    """
    word net generator.
    """
    def __init__(self):
        """
        initialize local variables.
        """
        self.coursename = None
        self.sourcefilepath = None
        self.neo4jdriver = Neo4jHandler.Neo4jHandler(None)
        self.sentence = SentenceReader.SentenceReader()
        #self.splitor = JiebaSplitor.JiebaSplitor()
        self.splitor = HanlpSplitor.HanlpSplitor()
        #self.cypherlist = []
        self.sentcypherlist = []
        #self.cypherlist.append("CREATE CONSTRAINT ON (c:WORD) ASSERT c.name IS UNIQUE;")

        # course name

    def generateNode(self):
        if self.sourcefilepath is None:
            return

        # 检查是否已经创建过该课程，如果已经创建，则直接返回
        hasexist = self.isCreateTheCourse()
        if hasexist == True:
            return


        # 删除已有的内容
        #self.neo4jdriver.cypherexecuter("match (n:WORD)-[r:NEXT]-(m:WORD) delete r;")
        #self.neo4jdriver.cypherexecuter("match (n:WORD) delete n;")

        # 创建约束
        self.neo4jdriver.cypherexecuter("CREATE CONSTRAINT ON (c:WORD) ASSERT c.name IS UNIQUE;")
        sentencecount = 0
        for cypherstatement in self.generateCypher():
            sentencecount = sentencecount + 1
            print 'sentence index : ' + str(sentencecount)
            print cypherstatement
            self.neo4jdriver.cypherexecuter(cypherstatement)
            print 'push one sentence over.'

        # 如果没有创建过该课程，则创建该课程
        self.createTheCourse()
        print 'push over.'

    def createTheCourse(self):
        """
        创建课程节点
        :param coursename: 
        :return: 
        """
        if self.coursename is None:
            return
        # 创建约束
        self.neo4jdriver.cypherexecuter("CREATE CONSTRAINT ON (c:COURSE) ASSERT c.name IS UNIQUE;")
        cypherstatement = "MERGE (c:COURSE {{name: '{0}'}})".format(self.coursename)
        self.neo4jdriver.cypherexecuter(cypherstatement)

    def isCreateTheCourse(self):
        """
        是否该课程已经创建
        :param coursename: 
        :return: 
        """
        hasExist = False
        if self.coursename is None:
            return hasExist

        cypher = "match(n:COURSE) where n.name in ['{0}'] return n.name as name".format(self.coursename)
        result = self.neo4jdriver.cypherexecuter(cypher)
        for record in result:
            name = record['name']
            hasExist = True
        return hasExist

    def generateCypher(self):
        """
        generate cypher statement
        :return: 
        """

        for sentence in self.sentence.getSentence(self.sourcefilepath):
            wordlist = self.splitor.split(sentence)

            length = len(wordlist)
            if length == 0:
                continue

            self.sentcypherlist = []
            # 处理同层的概念，同层的概念直接建立关系
            index = 0
            posindex = 0
            for poslist in wordlist:

                # 同层，也就是词性相同的词，是并列关系，他们直接相互存在关系
                self.createRelationLayerInner(poslist, index)
                index = index + 1


            # 如果wordlist后面还有，则建立关系，不同层之间建立关系
            index= 0
            while index < length - 1:
                self.createRelationLayerOuter(wordlist[index],wordlist[index+1],index)
                index += 1

            yield '\r\n'.join(self.sentcypherlist) + ';'
            #self.cypherlist.append(cypherstatement)


    def createRelationLayerInner(self, poslist,index):
        """
        同层概念之间建立关系
        :param poslist: 
        :param index: 
        :return: 
        """
        poslength = len(poslist)
        seq = str(index)
        cypher = []
        if poslength > 1:
            posindex = 0

            while posindex < poslength:
                # create node cypher
                nseq = seq + str(posindex)
                wns = "MERGE (w{0}:WORD {{name: '{1}'}})".format(nseq,poslist[posindex])
                cypher.append(wns)
                posindex += 1

            posindex = 0
            while posindex < poslength - 1:
                # create relation cypher
                subposlist = poslist[posindex:]
                sublength = len(subposlist)
                for subposindex in range(1, sublength):
                    start_seq = seq + str(posindex)
                    end_seq = seq + str(posindex + subposindex)
                    rns = "MERGE (w{0})-[:NEXT]->(w{1})".format(start_seq, end_seq)
                    cypher.append(rns)
                posindex += 1
        else:
            nseq = seq + str(0)
            wns = "MERGE (w{0}:WORD {{name: '{1}'}})".format(nseq,poslist[0])
            cypher.append(wns)

        cypherstatement = '\r\n'.join(cypher)
        self.sentcypherlist.append(cypherstatement)

    def createRelationLayerOuter(self, poslist, nextposlist,index):
        pre_seq = str(index)
        aft_seq = str(index + 1)
        pre_length = len(poslist)
        aft_length = len(nextposlist)
        cypher = []
        # 2层循环
        for pre_index in range(pre_length):
            start_seq = pre_seq + str(pre_index)
            for aft_index in range(aft_length):
                end_seq = aft_seq + str(aft_index)
                rns = "MERGE (w{0})-[:NEXT]->(w{1})".format(start_seq, end_seq)
                cypher.append(rns)
        if cypher:
            cypherstatement = '\r\n'.join(cypher)
            self.sentcypherlist.append(cypherstatement)

if __name__ == "__main__":
    sr = WordnetGenerator()
    #sr.generateCypher()
    sr.generateNode()
    print 'split over'