from __future__ import division, print_function
import first
import Pmf


def prob_early(pmf):
    return get_fraction_in_range(pmf, upper=38)


def prob_on_time(pmf):
    return get_fraction_in_range(pmf, lower=38, upper=41)


def prob_late(pmf):
    return get_fraction_in_range(pmf, lower=41)


def get_fraction_in_range(pmf, lower=-float('inf'), upper=float('inf')):
    '''
    Get the fraction of the number of entries in the PMF with values that
    lie in the half-open interval [lower, upper).

    '''
    count = sum(pmf.Prob(value) for value in pmf.Values() 
                if lower <= value < upper)
    return count


def get_relative_risks(pmf_firsts, pmf_others):
    prob_types = ('early', 'on time', 'late')
    result = {}
    for i, f in enumerate((prob_early, prob_on_time, prob_late)):
        try:
            result[prob_types[i]] = f(pmf_firsts) / f(pmf_others)
        except ZeroDivisionError:
            if f(pmf_firsts):
                result[prob_types[i]] = float('inf')
            else:
                result[prob_types[i]] = float('nan')
    return result



def main():
    live = first.get_live_pregnancies(first.get_pregnancies_dataset())
    firsts, others = first.split_one_vs_all(live, birthord=1)
    pmf_firsts = Pmf.MakePmfFromList(item.prglength for item in firsts)
    pmf_others = Pmf.MakePmfFromList(item.prglength for item in others)
    pmf_all = Pmf.MakePmfFromList(item.prglength for item in live)
    birth_types = ('first babies', 'subsequent babies', 'all live births')
    prob_types = ('early', 'on time', 'late')
    for i, pmf in enumerate((pmf_firsts, pmf_others, pmf_all)):
        for j, f in enumerate((prob_early, prob_on_time, prob_late)):
            print('The probability of {} being born {} is {} %'.format(
                birth_types[i], prob_types[j], f(pmf) * 100
            ))
    risks = get_relative_risks(pmf_firsts, pmf_others)
    print()
    for prob_type in prob_types:
        print('The relative risk of first babies to others arriving {} is {}'
              .format(prob_type, risks[prob_type]))

        
if __name__ == '__main__':
    main()
