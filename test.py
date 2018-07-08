import jieba

seg_list = jieba.cut(u" we come's from THU Tsinghua University. ")# -*- coding: utf-8 -*-
print("Full Mode: " + "/ ".join(seg_list))
