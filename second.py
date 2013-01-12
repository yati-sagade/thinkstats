from __future__ import print_function
from matplotlib import pyplot as plt
import numpy as np
import operator
import math
import first
import survey
import thinkstats
import Pmf as pmf


def main():
    pregnancies = first.get_pregnancies_dataset()
    live_pregnancies = [preg for preg in pregnancies.records if preg.outcome == 1]
    firsts, subsequents = first.split_one_vs_all(live_pregnancies, 
                                                 birthord=1)
    period_first = first.get_values_for_field(firsts, 'prglength')
    period_subsequent = first.get_values_for_field(subsequents, 'prglength')
    var_first = thinkstats.Var(period_first)
    var_second = thinkstats.Var(period_subsequent)

    print('Variance of the first children gestation periods: {} weeks^2'
          .format(var_first))
    print('\tAnd the sd is {} weeks.'.format(math.sqrt(var_first)))
    print('Variance of the subsequent children gestation periods: {} weeks^2'
          .format(var_second))
    print('\tAnd the sd is {} weeks.'.format(math.sqrt(var_second)))

    weights = get_pumpkin_weights()
    print('Finding the variance and mean for these pumpkins: {}'
          .format(weights))
    mu, var = pumpkins(weights)
    sd = math.sqrt(var)
    print('\tmean = {}\tvariance = {}\tsd = {}'.format(mu, var, sd))
    bar_chart(pregnancies)
    plot_pregnancy_pmf(pregnancies)
    plot_pregnancies_pmf_differences(pregnancies)


get_pumpkin_weights = lambda: (1, 1, 1, 3, 3, 591)


def mode(hist, multiple_modes=False):
    '''
    Get the mode of a Pmf.Hist

    '''
    maxfreq = hist.MaxLike()
    values = [val for val, freq in hist.Items() if freq == maxfreq]
    if len(values) > 1 and multiple_modes:
        return values
    return values[0]


def all_modes(hist):
    return sorted(hist.Items(), key=operator.itemgetter(1, 0), reverse=True)


def pumpkins(weights):
    return thinkstats.MeanVar(weights)

def bar_chart(pregnancies):
    live_pregnancies = first.get_live_pregnancies(pregnancies)
    firsts, seconds = first.split_one_vs_all(live_pregnancies, birthord=1)
    period_first = first.get_values_for_field(firsts, 'prglength')
    period_second = first.get_values_for_field(seconds, 'prglength')
    hist1 = pmf.MakeHistFromList(period_first)
    hist2 = pmf.MakeHistFromList(period_second)

    fig = plt.figure()
    ax = fig.add_subplot(111)
    width = 0.35
    x1, y1 = hist1.Render()
    x2, y2 = hist2.Render()
    r1 = ax.bar(x1, y1, width, color='blue')
    r2 = ax.bar(np.array(x2) + width, y2, width, color='grey')
    ax.set_xlabel('Gestation period(weeks)')
    ax.set_ylabel('Frequency')
    ax.set_title('Comparison of the gestation periods of first and subsequent'
                 ' babies')
    ax.legend((r1[0], r2[0]), ('First Babies', 'Subsequent Babies'))
    plt.show()


def remaining_lifetime(lifetime_pmf, age=0):
    '''
    Get a Pmf of remaining lifetimes of a component whose liftime Pmf and 
    age are given.

    '''
    ret = pmf.Pmf()
    for value, prob in lifetime_pmf.Items():
        ret.Set(value-age, prob)
    return ret


def pmf_mean(f):
    '''
    Calculate the mean from a Pmf.
    Args:
        f: a Pmf.Pmf object

    '''
    return sum(pi * xi for xi, pi in f.Items())


def pmf_var(f):
    '''
    Calculate the variance from a Pmf.
    Args:
        f: a Pmf.Pmf object

    '''
    mu = pmf_mean(f)
    var = 0.0
    for value, prob in f.Items():
        diff = value - mu
        diff_sq = diff * diff
        var += prob * diff_sq
    return var

def plot_pregnancy_pmf(prg):
    live_prg  = first.get_live_pregnancies(prg)
    firsts, subsequents = first.split_one_vs_all(live_prg, birthord=1)
    first_prglen = [record.prglength for record in firsts]
    subsequent_prglen = [record.prglength for record in subsequents]
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    width = 0.35
    
    p1, p2 = map(pmf.MakePmfFromList, (first_prglen, subsequent_prglen))
    x1, y1 = p1.Render()
    x2, y2 = p2.Render()

    r1 = ax.bar(x1, y1, width, color='blue')
    r2 = ax.bar(np.array(x2) + width, y2, width, color='grey')
    ax.set_xlabel('Gestation period(weeks)')
    ax.set_ylabel('Probability')
    ax.set_title('Comparison of the gestation periods of first and subsequent'
                 ' babies')
    ax.legend((r1[0], r2[0]), ('First Babies', 'Subsequent Babies'))
    plt.show()


def plot_pmf_scatter_plot(p, color='r+', axis_labels=None, legend=None, 
                          title=None):
    '''
    Plot a Pmf.Pmf object as a scatter plot with the gestatio period in weeks
    on the horizontal axis and the probability on the vertical axis.
    Args:
        p(Pmf.Pmf): The PMF to plot.
        axis_labels(2-tuple): The labels to give to the horizontal and the
                              vertical axes, respectively.
        legend(str): The legend for this scatter plot.

    '''
    xs, ys = p.Render()

    fig = plt.figure()
    ax = fig.add_subplot(111)
    r = ax.plot(xs, ys, color)
    if axis_labels is not None:
        ax.set_xlabel(axis_labels[0])
        ax.set_ylabel(axis_labels[1])
    if legend is not None:
        ax.legend((r[0],), (legend,))
    if title is not None:
        ax.set_title(title)
    plt.show()


def plot_pregnancies_pmf_differences(prg, week_lo=35, week_hi=46):
    live_prg  = first.get_live_pregnancies(prg)
    firsts, subsequents = first.split_one_vs_all(live_prg, birthord=1)
    first_prglen = [record.prglength for record in firsts]
    subsequent_prglen = [record.prglength for record in subsequents]
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    p1 = pmf.MakePmfFromList(first_prglen)
    p2 = pmf.MakePmfFromList(subsequent_prglen)
    result = {week: 100 * (p1.Prob(week) - p2.Prob(week))
              for week in xrange(week_lo, week_hi)}
    ax.bar(result.keys(), result.values(), width=1., color='blue') 
    ax.set_title('Percent differences in probabilities of gestation periods')
    ax.set_xlabel('Gestation period(weeks)')
    ax.set_ylabel('100(Pfirst - Psubsequent)')
    plt.show()
        



    



if __name__ == '__main__':
    main()



