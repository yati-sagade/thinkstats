import numpy as np
import Pmf
from matplotlib import pyplot as plt
from first import (get_live_pregnancies, get_pregnancies_dataset,
                   split_one_vs_all)


def probability_of_birth_in_week(pmf, week):
    '''
    Get the probability that a birth will happen in week |week|, given that
    it has not happened before it.
    Args:
        pmf(Pmf.Pmf): The PMF of pregnancies.

    '''
    my_pmf = pmf.Copy()
    for value in my_pmf.Values():
        if value < week:
            my_pmf.Remove(value)
    my_pmf.Normalize()
    return my_pmf.Prob(week)


if __name__ == '__main__':
    live_pregnancies = get_live_pregnancies(get_pregnancies_dataset())
    firsts, others = split_one_vs_all(live_pregnancies,
                                      birthord=1)
    first_durations = [record.prglength for record in firsts]
    others_durations = [record.prglength for record in others]
    first_pmf = Pmf.MakePmfFromList(first_durations)
    others_pmf = Pmf.MakePmfFromList(others_durations)
    fig = plt.figure()
    sp = fig.add_subplot(111)
    # weeks1, weeks2 = (range(min(first_durations), max(first_durations)),
    #                   range(min(others_durations), max(others_durations)))
    weeks1, weeks2 = map(lambda t: range(*t), ((36, 45), (36, 45)))
    probs_first = [probability_of_birth_in_week(first_pmf, week)
                   for week in weeks1]
    probs_others = [probability_of_birth_in_week(others_pmf, week)
                    for week in weeks2]
    r1 = sp.plot(weeks1, probs_first, color='b')
    r2 = sp.plot(weeks2, probs_others, color='r')
    sp.legend((r1[0], r2[0]), ('first babies', 'subsequent babies'))
    sp.set_title('Conditional probabilities of first and subsequent babies'
                 ' against the pregnancy durations.')
    sp.set_xlabel('Pregnancy duration in weeks')
    sp.set_ylabel('Conditional probability of birth'
                  ' P(w|birth did not happen before week w')
    sp.grid()
    plt.show()



