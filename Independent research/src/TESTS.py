import Leap, sys, thread, time
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture

import sys, os, msvcrt

import numpy as np
from scipy.stats import truncnorm
import matplotlib.pyplot as plt


def compute_prob(xo=0, yo=0, sd=100):
    yo = -yo
    sd_left = (-100 - xo) / sd
    sd_right = (100 - xo) / sd
    sd_bottom = (-100 - yo) / sd
    sd_top = (100 - yo) / sd
    x = np.linspace(-100, 100, 201)
    y = np.linspace(-100, 100, 201)
    xx, yy = np.meshgrid(x, y)
    xx_pdf = truncnorm.pdf(xx, sd_left, sd_right, loc=xo, scale=sd)
    yy_pdf = truncnorm.pdf(yy, sd_bottom, sd_top, loc=yo, scale=sd)
    pdf = xx_pdf * yy_pdf
    prob = np.zeros([4, 4])
    for i in np.arange(4):
        i0 = 50 * i
        for j in np.arange(4):
            j0 = 50 * j
            prob[i, j] = pdf[i0:i0 + 50, j0:j0 + 50].sum()
    return prob

def main():
    prob = compute_prob(xo=0, yo=0, sd=50)
    print np.round(prob, 6)
    print
    print'sum of prob = %f' % prob.sum()
    plt.pcolor(prob[::-1, :])
    plt.axes().set_aspect('equal')
#-----------------------------------------------------------------------
# If this module is running at the top level (as opposed to being
# imported by another module), then call the 'main' function.
#-----------------------------------------------------------------------
if __name__ == '__main__':
    main()
