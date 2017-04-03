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
    lut = lookup()
    query = (Post
             .select(Post.user, fn.Count(Post.id).alias('quantity'))
             .group_by(Post.user)
             .order_by(fn.Count(Post.id).desc()))
    total = sum(int(row.quantity) for row in query)
    assert total == 18967
    print('# User Quantity Table')
    print('UID', 'Name', 'Quantity', 'Percentage', sep=' | ')
    print('---', '---', '---', '---', sep=' | ')
    for row in query:
        print(row.user, lut[row.user], row.quantity, "{:.2f}%".format(row.quantity/total*100), sep=' | ')

if __name__ == '__main__':
    sys.stdout = open('user_quantity_table.md', 'w')
    build()
    sys.stdout = sys.__stdout__
