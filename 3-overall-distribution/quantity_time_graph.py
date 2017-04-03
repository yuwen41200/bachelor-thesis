#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import Counter

import dateutil.parser
import pandas as pd

from models import *


def draw():
    times = []
    for post in Post.select():
        time = dateutil.parser.parse(post.time)
        times.append(time.date())
    time_counts = Counter(times)
    ts = pd.Series(time_counts)
    ts.plot()

if __name__ == '__main__':
    draw()
