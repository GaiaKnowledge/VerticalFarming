# coding=utf-8
from datetime import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta
import pandas as pd
import numpy as np
import random
import math
from math import pi
import matplotlib.pyplot as plt
import pba
import matplotlib.pyplot as plt

def pnt(a):
    if type(a) == pba.pbox.Pbox:
        return (a.mean_left + a.mean_right) / 2
    elif type(a) == list:
        return [pnt(b) for b in a]
    else:
        return (a)

def rng(a):
    if type(a) == pba.pbox.Pbox:
        # return pba.Interval(a.mean_left, a.mean_right)
        # return pba.Interval(a.mean_left-np.sqrt(a.var_right),
        #                    a.mean_right+np.sqrt(a.var_right))
        return a.get_interval(0.025, 0.975)
    elif type(a) == list:
        return [rng(b) for b in a]  # rng = pnt before
    else:
        return (a)

def pltem(ax, t, y, simple=True, label=None, shade=None):
    if simple:
        y = [rng(v) for v in y]  # Could be: y = rng(y). does the same as rng function when list
        # y1 = [v.left() for v in y]
        y1 = []
        for v in y:
            if type(v) == int or type(v) == float:
                y1 = y1 + [v]
            else:
                y1 = y1 + [v.left()]
        y2 = []
        for v in y:
            if type(v) == int or type(v) == float:
                y2 = y2 + [v]
            else:
                y2 = y2 + [v.right()]
        ax.plot(t, y2, label='Best Case {}'.format(label))
        ax.plot(t, y1, label='Worst Case {}'.format(label))
        if shade == True:
            ax.fill_between(t, y1, y2, alpha=0.2)
    else:
        pass