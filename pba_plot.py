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

def cut(B, p):
    p = int(p * pba.Pbox.STEPS)
    if type(B) in [int, float]: return B
    if type(B) == pba.interval.Interval: return B
    if type(B) == pba.pbox.Pbox: return pba.I(B.left[p], B.right[p])


def median(B):
    return cut(B, 0.5)


def minmaxmean(minimum, maximum, mean):
    return pba.mmms(minimum, maximum, mean, pba.I(0, ((mean - minimum) * (maximum - mean))) ** 0.5)


def minmaxmedian(minimum, maximum, median):
    ml = (minimum + median) / 2
    mr = (median + maximum) / 2
    vl = 0
    vr = (maximum - minimum) ** 2 / 4
    n = pba.Pbox.STEPS
    n1 = int(n / 2)
    if n1 + n1 == n:
        n2 = n1
    else:
        n2 = n1 + 1
    L = [minimum] * n2 + [median] * n1
    R = [median] * n1 + [maximum] * n2
    return pba.Pbox(np.array(L), np.array(R), mean_left=ml, mean_right=mr, var_left=vl, var_right=vr)

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

def med_pbox(a):
    if type(a) == pba.pbox.Pbox:
        # return pba.Interval(a.mean_left, a.mean_right)
        # return pba.Interval(a.mean_left-np.sqrt(a.var_right),
        #                    a.mean_right+np.sqrt(a.var_right))
        return median(a)
    elif type(a) == list:
        return [median(b) for b in a]  # rng = pnt before
    else:
        return (a)

def pltem(ax, t, y, simple=True, label=None, shade=None):
        if simple:
            y = [rng(v) for v in y]  # Could be: y = rng(y). does the same as rng function when list
            # y1 = [v.left() for v in y]
            y1 = []
            for v in y:
                if type(v) == int or type(v) == float or type(v) == np.float64:
                    y1 = y1 + [v]
                else:
                    y1 = y1 + [v.left]
            y2 = []
            for v in y:
                if type(v) == int or type(v) == float or type(v) == np.float64:
                    y2 = y2 + [v]
                else:
                    y2 = y2 + [v.right]
            ax.plot(t, y2, label='Max {}'.format(label), lw=3, c='k')
            ax.plot(t, y1, label='Min {}'.format(label), lw=3, c='k')
            if shade == True:
                ax.fill_between(t, y1, y2, alpha=0.2, facecolor='black')
        else:
            pass


def pltem_med(ax, t, y, simple=True, label=None, shade=None):
   # print(type(y[-1]))
    #if type(y[-1]) == pba.pbox.Pbox or type(y[-1]) == pba.interval.Interval:
        if simple:
            y = [med_pbox(v) for v in y]  # Could be: y = rng(y). does the same as rng function when list
            # y1 = [v.left() for v in y]
            y1 = []
            for v in y:
                if type(v) == int or type(v) == float or type(v) == np.float64:
                    y1 = y1 + [v]
                else:
                    y1 = y1 + [v.left]
            y2 = []
            for v in y:
                if type(v) == int or type(v) == float or type(v) == np.float64:
                    y2 = y2 + [v]
                else:
                    y2 = y2 + [v.right]
            ax.plot(t, y2, label='Upper Median', c='0', lw=1.5, linestyle=':')
            ax.plot(t, y1, label='Lower Median', c='0', lw=1.5, linestyle=':')
            if shade == True:
                ax.fill_between(t, y1, y2, alpha=0.6, facecolor='grey')
        else:
            pass
    #else:
    #    ax.plot(t, y, label='{}'.format(label), lw=2, c='k')

