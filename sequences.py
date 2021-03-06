import itertools
from operator import itemgetter
import csv
# import pandas as pd
"""
Script to generate alternating sequences of specified length, and perform switches.
"""

'''
#################
#GENERAL UTILITY#
#################
'''

def flatten(lis):
    '''Given a list, possibly nested to any level, return it flattened.'''
    new_lis = []
    for item in lis:
        try:
            if type(item[0]) == type([]):
                new_lis.extend(flatten(item))
            else:
                new_lis.append(item)
        except TypeError:
            new_lis.append(item)
    return new_lis


def find_duplicates(res):
    '''
    Finds duplicate patterns by iterating over the result of perform_swaps
    '''
    initial_seqs = {}
    for k,v in res.items():
        for i, v1 in v.items():        
            if v1 in initial_seqs.keys():
                res[k][i] = '[' + v1 + ']'
                if '[' not in res[initial_seqs[v1][0]][initial_seqs[v1][1]]:
                    res[initial_seqs[v1][0]][initial_seqs[v1][1]] = '['+v1+']'
            else:
                initial_seqs[v1] = (k, i)
                continue
    return res

'''
#################################
#SEQUENCE AND PATTERN GENERATION#
#################################
'''


def gen_sequence(l, cur_seq, next_gt):
    # Start by getting list of remaining numbers in the sequence.
    if len(cur_seq)<len(l):
        remaining = [x for x in l if x not in cur_seq]
        true_remain = []
        for i in remaining:
            if next_gt and cur_seq[-1]<i:
                true_remain.append(i)
            elif not next_gt and cur_seq[-1]>i:
                true_remain.append(i)
        if len(true_remain)==0:
            return cur_seq
        else:            
            return [gen_sequence(l, cur_seq + [x], not next_gt) for x in true_remain]
    else:
        return cur_seq


def gen_patterns(n):
    l = '()*'
    combos = list(itertools.product([')', '(','*'], repeat=n))
    bad = ['((','))', '(*', '*)']
    temp = []
    for i in combos:
        if not any(b in ''.join(i) for b in bad):
            if i[0] != ')' and i[-1]!='(':
                temp.append(list(i))
    return temp

'''
################
#SWAP EXECUTION#
################
'''


def pattern_seq(seq, pat):
    '''
    Pattern_seq takes in an indiviual sequence and an individual swap pattern, and applies the swap pattern to the sequence.

    :param seq: alternating  sequence
    :param pat: swap pattern
    :return: swapped sequence
    '''
    ret = seq[:]
    for i in range(len(pat)):
        if pat[i] == '(':
            ret[i], ret[i+1] = ret[i+1], ret[i]
    return ret


def perform_swaps(seqs, pats):
    '''
    Iterates over the lists of sequences, builds a nested dictionary of the form {alternating sequence: {swap pattern: swapped sequence}}

    :param seqs: list of sequences
    :param pats: list of swap patterns
    :return: nested dictionary
    '''
    results = {}
    for seq in seqs:
        str_seq = ''.join([str(x) for x in seq])
        results[str_seq] = {}
        for pat in pats:
            results[str_seq][''.join(pat)] = ''.join([str(x) for x in pattern_seq(seq, pat)])
    return results





def main():
    says = eval(input("enter an n: "))
    results = {}
    total_list = []
    for i in range(1, says):
        zed = flatten(gen_sequence(list(range(1, says+1)), [i], True))
        results[str(i)] = [x for x in zed if len(x) == says]
        total_list.extend(results[str(i)])
    pats = gen_patterns(says)
    print("number of alternating sequences %d \n" % len(total_list))
    print("number of swap patterns: %d \n" % len(pats))
    performed = perform_swaps(total_list, pats)
    # print(performed)
    outfile = 'output_n_%s.csv' % str(says)
    performed = find_duplicates(performed)
    with open(outfile, 'w') as f:
        writer = csv.DictWriter(f, fieldnames=[''.join(x) for x in pats][::-1])
        writer.writeheader()
        for key, val in sorted(performed.items()):
            row = {'*'*says: key}
            print([n for n in val.items() if '[' in n[1]])
            row.update(val)
            writer.writerow(row)

if __name__ == '__main__':
    main()