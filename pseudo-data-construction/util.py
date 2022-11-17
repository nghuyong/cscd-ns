#!/usr/bin/env python
# encoding: utf-8
"""
File Description:
Author: rightyonghu
Created Time: 2022/9/6
"""
import pickle

import kenlm
import pypinyin
from LAC import LAC

UNK_VOCAB = '[UNK]'
NULL_VOCAB = '[NULL]'
PINYIN_DISTANCE_MATRIX = pickle.load(open('../data/resource/pinyin_distance_matrix.pkl', 'rb'))
VALID_PINYIN = {a for (a, b) in PINYIN_DISTANCE_MATRIX.keys()}
lac = LAC(mode='lac')
lm = kenlm.Model('../data/resource/char_4_gram.bin')


class PinyinInfo:
    """
    pinyin info
    """

    def __init__(self, sentence):
        self.sentence = sentence
        self.pinyin_list = list()
        self.initial_list = list()
        self.final_list = list()
        self.pinyin_list_str = None
        self.index_of_pinyin_str_to_index_of_sentence = dict()

    def add_pinyin(self, add_initial_final=False):
        """
        add pinyin to sentence
        :param add_initial_final: whether to add initial and final info
        :return:
        """
        pinyin_list = pypinyin.lazy_pinyin(self.sentence)
        initials, finals = [], []
        if add_initial_final:
            initials = pypinyin.lazy_pinyin(self.sentence, style=pypinyin.Style.INITIALS)
            initials = [initial if initial else NULL_VOCAB for initial in initials]
            finals_and_tones = pypinyin.lazy_pinyin(self.sentence, style=pypinyin.Style.FINALS_TONE3)
            finals_and_tones = [each if each else '[UNK]' for each in finals_and_tones]
            finals = [finals_and_tone[:-1] if finals_and_tone[-1].isnumeric() else finals_and_tone
                      for finals_and_tone in finals_and_tones]
        char_index = 0
        for i, pinyin in enumerate(pinyin_list):
            if pinyin in VALID_PINYIN and self.sentence[char_index] != pinyin[0]:
                self.pinyin_list.append(pinyin)
                if add_initial_final:
                    self.initial_list.append(initials[i])
                    self.final_list.append(finals[i])
                char_index += 1
            else:
                self.pinyin_list.extend([UNK_VOCAB for _ in pinyin])
                if add_initial_final:
                    self.initial_list.extend([UNK_VOCAB for _ in pinyin])
                    self.final_list.extend([UNK_VOCAB for _ in pinyin])
                char_index += len(pinyin)
        self.pinyin_list_str = ",".join(self.pinyin_list)

    def align_pinyin_str_to_sentence(self):
        """
        align pinyin to origin char
        :return:
        """
        assert self.pinyin_list_str is not None
        self.index_of_pinyin_str_to_index_of_sentence = {i: -1 for i in range(len(self.pinyin_list_str))}
        index_of_pinyin_str = 0
        index_of_sentence = 0
        for pinyin in self.pinyin_list:
            if pinyin is not UNK_VOCAB:
                for j, _ in enumerate(pinyin):
                    self.index_of_pinyin_str_to_index_of_sentence[index_of_pinyin_str + j] = index_of_sentence
            index_of_pinyin_str += len(pinyin)
            index_of_pinyin_str += 1  # 拼音之间的逗号
            index_of_sentence += 1


def seg(sent):
    """
    seg sentence by LAC
    :param sent: sentence
    :return: [(word,start,end), ... ]
    """
    word_list = []
    idx = 0
    seg_sent = lac.run(sent)[0]
    for s in seg_sent:
        word_list.append((s, idx, idx + len(s)))
        idx += len(s)
    return word_list


def is_chinese_char(c):
    """
    whether the char is Chinese
    :param c:
    :return:
    """
    if len(c) > 1:
        return False
    return '\u4e00' <= c <= '\u9fa5'


def is_chinese_string(s):
    """
    whether the text is Chinese
    :param s: text
    :return:
    """
    return all(is_chinese_char(c) for c in s)


def cal_ppl(s):
    """
    calculate char level ppl of text
    :param s:
    :return:
    """
    return lm.perplexity(' '.join(list(s)))


def is_nearby_pinyin(p1, p2):
    """
    whether p1 and p2 is nearby in the keyboard
    :param p1:
    :param p2:
    :return:
    """
    t9_keyboard = {
        'a': (0, 1), 'b': (0, 1), 'c': (0, 1),
        'd': (0, 2), 'e': (0, 2), 'f': (0, 2),
        'g': (1, 0), 'h': (1, 0), 'i': (1, 0),
        'j': (1, 1), 'k': (1, 1), 'l': (1, 1),
        'm': (1, 2), 'n': (1, 2), 'o': (1, 2),
        'p': (2, 0), 'q': (2, 0), 'r': (2, 0), 's': (2, 0),
        't': (2, 1), 'u': (2, 1), 'v': (2, 1),
        'w': (2, 2), 'x': (2, 2), 'y': (2, 2), 'z': (2, 2)
    }

    t26_keyboard = {'q': (0, 0), 'w': (0, 1), 'e': (0, 2), 'r': (0, 3), 't': (0, 4), 'y': (0, 5), 'u': (0, 6),
                    'i': (0, 7), 'o': (0, 8), 'p': (0, 9),
                    'a': (1, 0), 's': (1, 1), 'd': (1, 2), 'f': (1, 3), 'g': (1, 4), 'h': (1, 5), 'j': (1, 6),
                    'k': (1, 7), 'l': (1, 8),
                    'z': (2, 0), 'x': (2, 1), 'c': (2, 2), 'v': (2, 3), 'b': (2, 4), 'n': (2, 5), 'm': (2, 6)}
    diff_c = [(c1, c2) for c1, c2 in zip(p1, p2) if c1 != c2]
    c1, c2 = diff_c[0]
    d_x = abs(t26_keyboard[c1][0] - t26_keyboard[c2][0])
    d_y = abs(t26_keyboard[c1][1] - t26_keyboard[c2][1])
    if d_x + d_y == 1:
        return True
    if t9_keyboard[c1] == t9_keyboard[c2]:
        return True
    return False


if __name__ == '__main__':
    pinyin_info = PinyinInfo('欢迎大家加入QQ群：64942796一起分享你的吐槽创意！')
    pinyin_info.add_pinyin()
    print(pinyin_info.pinyin_list)
