from __future__ import print_function
import survey


def main():
    table = get_pregnancies_dataset() 
    print('Total number of pregnancies: {}'.format(len(table.records)))
    live_pregnancies = get_live_pregnancies(table)
    print('Total pregnancies that resulted in live births: {}'
          .format(len(live_pregnancies)))
    # Partition the pregnancies in two sets - one for the first child and the
    # other for subsequent childs.
    first_children, second_children = split_one_vs_all(live_pregnancies,
                                                       birthord=1)
    nf, ns = len(first_children), len(second_children)
    total_percent = 100.0 / (nf + ns)
    print('Total live first pregnancies: {} ({}%)'
          .format(nf, nf * total_percent))

    print('Total live non-first pregnancies: {} ({}%)'
          .format(ns, ns * total_percent))

    print('-' * 80)
    first_pregnancy_lengths = [record.prglength for record in first_children]
    second_pregnancy_lengths = [record.prglength for record in second_children]
    mu1, mu2 = [mean(item) 
                for item in
                (first_pregnancy_lengths, second_pregnancy_lengths)]
    print('Average first pregnancy length: {} weeks.'
          .format(mu1))
    print('Average second pregnancy length: {} weeks.'
          .format(mu2))
    
    print('It looks like the average first pregnancy is {} than the average '
          'other pregnancies by {} days'.format(
              'shorter' if mu1 < mu2 else 'longer',
              abs((mu1 - mu2) * 7)
          )
    )



def mean(items):
    return float(sum(items)) / len(items) if items else 0.0


def get_pregnancies_dataset():
    table = survey.Pregnancies()
    table.ReadRecords()
    return table


def split_one_vs_all(data, **field_values):
    '''
    Split a given dataset(data) into two subgroups. `field_values` is a dict 
    of the form {field1: val1, field2: val2...}. Of the resulting two
    partitions, the first one will have the values supplied here and the other
    group will contain all other records. 

    '''
    if not field_values:
        return data, []
    first, second = [], []
    for record in data:
        the_one = first
        for field, value in field_values.iteritems():
            if getattr(record, field) != value:
                the_one = second
                break
        the_one.append(record)
    return first, second


def get_live_pregnancies(table):
    '''
    Return a list of pregnancies resulting in a live birth.

    '''
    return [record for record in table.records if record.outcome == 1] 


def get_values_for_field(data, field):
    return [getattr(record, field) for record in data]

if __name__ == '__main__':
    main()

