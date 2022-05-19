#!/usr/bin/python
#-*-coding:utf-8 -*-
#Version  : 1.0
#Filename : parse_dep.py
from __future__ import print_function

import json
import math
from collections import defaultdict
import sys


def main(order):
    # sents = []
    cand_name = "data/selected_syn_noun_pairs.txt"
    dep_name = "data/dep_selected_syn_noun_pairs.txt"
    order = int(order)
    left = math.ceil(order / 2)
    right = order - left
    cands = set()
    pair_records = []
    dep_records = defaultdict(lambda : defaultdict(int))

    with open(cand_name) as reader:
        for line in reader:
            words = line.strip().split()
            pair_records.append(words)
            cands.update(set(words))

    words = []
    tgts = []
    poss = []
    sents = 0

    with open(dep_name) as reader:
        for line in reader:
            line = line.strip()
            if line == "====================":
                #sents += 1
                #if sents > 1000:
                #    break
                pass
            elif line == "--------------------":
                for tgt in tgts:
                    before = (["none", "none"] + poss[:tgt])[-left:]
                    after = (poss[tgt:]+["none", "none"])[1:1+right]
                    key = tuple(before + after)
                    dep_records[words[tgt]][key] += 1

                words = []
                poss = []
                tgts = []
            else:
                line = line.split("\t")
                word_id = line[0].split(":", 1)[1].strip()
                word = line[1].split(":", 1)[1].strip()
                words.append(word)
                pos = line[-1].split(":", 1)[1].strip()
                poss.append(pos)
                if pos == "NOUN" and word in cands:
                    tgts.append(int(word_id)-1)
    for word, syn in pair_records:
        keys = list(set(dep_records[word].keys()) & set(dep_records[syn]))
        original = [(key, dep_records[word][key], dep_records[syn][key]) for key in keys]
        print(original)

if __name__ == "__main__":
    main(sys.argv[1])
