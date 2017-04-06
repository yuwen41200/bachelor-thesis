#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import json

from models import *


def lookup():
    lut_location = os.path.join('..', '1-data-collection', 'dat', 'uid_to_name_map.dat')
    with open(lut_location) as file:
        lut = json.load(file)
    return lut


def build():
    no = 0
    lut = lookup()
    for kw in Keyword.select():
        no += 1
        if no == 1:
            print('# Keywords by User')
            print('Name', '#0', '#1', '#2', '#3', '#4', '#5', '#6', '#7', '#8', '#9', sep=' | ')
            print('---', '---', '---', '---', '---', '---', '---', '---', '---', '---', '---', sep=' | ')
        elif no == 129:
            print('# Keywords by Time')
            print('Period', '#0', '#1', '#2', '#3', '#4', '#5', '#6', '#7', '#8', '#9', sep=' | ')
            print('---', '---', '---', '---', '---', '---', '---', '---', '---', '---', '---', sep=' | ')
        elif no == 142:
            print('# Keywords by None')
            print('---', '#0', '#1', '#2', '#3', '#4', '#5', '#6', '#7', '#8', '#9', sep=' | ')
            print('---', '---', '---', '---', '---', '---', '---', '---', '---', '---', '---', sep=' | ')
        if no <= 128:
            print(
                lut[kw.subject], kw.rank0, kw.rank1, kw.rank2, kw.rank3, kw.rank4,
                kw.rank5, kw.rank6, kw.rank7, kw.rank8, kw.rank9, sep=' | '
            )
        else:
            print(
                kw.subject, kw.rank0, kw.rank1, kw.rank2, kw.rank3, kw.rank4,
                kw.rank5, kw.rank6, kw.rank7, kw.rank8, kw.rank9, sep=' | '
            )

if __name__ == '__main__':
    sys.stdout = open('keyword_table.md', 'w')
    build()
    sys.stdout = sys.__stdout__
