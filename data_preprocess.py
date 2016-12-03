# -*- coding: utf-8 -*-
from __future__ import print_function

import re
from operator import itemgetter
import jieba
import jieba.analyse
import jieba.posseg as pseg
import Params


class DataPreProcess:
    def __init__(self, ad_text, user_ad):
        self.init_text = ad_text         # (initial text) ad_id : title
        self.user_ad = user_ad
        self.topK = Params.tagNum            # number of tags
        self.word_num = Params.wordNum
        self.ad_Tag = Params.ad_Tag           # number of tags in each ad
        self.user_Tag = Params.user_Tag
        self.relation_ad = Params.TAGRELATION_AD
        self.relation_user = Params.TAGRELATION_USER
        self.title = str()
        self.tag_weight = dict()       # tag : weight
        self.ad_tags = dict()           # ad : tags
        self.user_tags = dict()         # user : tags
        self.ad_text = dict()
        self.tag_relation = dict()

        for ad in ad_text.keys():
            self.ad_text[ad] = ad_text[ad][0]

        jieba.enable_parallel(4)

    # use punctuations to segment title
    def dot_seg(self):
        for ad in self.ad_text.keys():
            r = '[!"#$%&\'()*+,-./:;<=>?@，。★、…【】¥&＊：？；［］｛｝＝－——（）……％＃@《》？“”‘’！[\\]^_`#￥{|}～！＋]+'
            split = re.split(r, self.ad_text[ad])
            for word in split:
                if word != "":
                    self.title += word
        return

    def tag_extract(self):
        title = self.title
        tags = jieba.analyse.extract_tags(title, topK=self.topK, withWeight=True)
        for item in tags:
            self.tag_weight[item[0]] = item[1]
        return

    def ad_tag(self):
        for ad, text in self.ad_text.items():
            temp = dict()
            c = pseg.cut(text)
            count = 0
            self.ad_tags.setdefault(ad, [('', 0)])
            for word, flag in c:
                if word in self.tag_weight.keys() and flag == 'n':
                    temp[word] = self.tag_weight[word]
                    count += 1
            if count == 0:
                continue

            self.ad_tags[ad] = sorted(temp.items(), key=itemgetter(1), reverse=True)[:self.ad_Tag]

            # tag relation based on ad
            tag_rel = dict()
            for tag_1 in self.ad_tags[ad]:
                tag_rel.setdefault(tag_1[0], {})
                for tag_2 in temp:
                    if tag_2[0] == tag_1[0]:
                        continue
                    tag_rel[tag_1[0]].setdefault(tag_2[0], 0)
                    tag_rel[tag_1[0]][tag_2[0]] += self.relation_ad
            self.tag_relation = tag_rel

    def user_tag(self):
        related_tags = dict()

        for user, ad_list in self.user_ad["VIEW"].items():
            related_tags.setdefault(user, {})
            for ad in ad_list:
                if ad not in self.ad_tags.keys():
                    continue
                for t_w in self.ad_tags[ad]:
                    related_tags[user].setdefault(t_w[0], [0, 0])
                    related_tags[user][t_w[0]][0] += 1
                    related_tags[user][t_w[0]][1] = t_w[1]

        for user, ad_list in self.user_ad["OTHER"].items():
            related_tags.setdefault(user, {})
            for ad in ad_list:
                if ad not in self.ad_tags.keys():
                    continue
                for t_w in self.ad_tags[ad]:
                    related_tags[user].setdefault(t_w[0], [0, 0])
                    related_tags[user][t_w[0]][0] += 2
                    related_tags[user][t_w[0]][1] = t_w[1]

        for user, ad_list in related_tags.items():
            self.user_tags[user] = list(sorted(related_tags[user].items(), key=itemgetter(1), reverse=True))[:self.user_Tag]
            for tag_1 in self.user_tags[user]:
                self.tag_relation.setdefault(tag_1[0], {})
                for tag_2 in self.user_tags[user]:
                    if tag_1 == tag_2:
                        continue
                    self.tag_relation[tag_1[0]].setdefault(tag_2[0], 0)
                    self.tag_relation[tag_1[0]][tag_2[0]] += self.relation_user

    #def recommendation(self):
        # linked to recommendation model :)
