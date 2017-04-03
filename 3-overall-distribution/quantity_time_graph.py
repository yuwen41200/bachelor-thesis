#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import Counter

import dateutil.parser
import pandas as pd
import matplotlib.style
import matplotlib.pyplot as plt

from models import *


def render_image(data):
    plt.clf()
    ts = pd.Series(data)
    ax = ts.plot()
    ax.set_xlabel('Time')
    ax.set_ylabel('Quantity')
    plt.gcf().autofmt_xdate()
    plt.savefig('quantity_time_graph.png', dpi=200, bbox_inches='tight')


def render_image_cum(data):
    plt.clf()
    ts = pd.Series(data)
    ts = ts.cumsum()
    ax = ts.plot()
    ax.set_xlabel('Time')
    ax.set_ylabel('Quantity')
    plt.gcf().autofmt_xdate()
    plt.savefig('quantity_time_cumulative_graph.png', dpi=200, bbox_inches='tight')


def draw():
    times = []
    for post in Post.select():
        time = dateutil.parser.parse(post.time)
        times.append(time.date())
    time_counts = Counter(times)
    render_image(time_counts)
    render_image_cum(time_counts)

if __name__ == '__main__':
    matplotlib.style.use('ggplot')
    draw()
