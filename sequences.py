import itertools
import csv
import pandas as pd
"""
Script to generate alternating sequences of specified length, and perform switches.
"""


def flatten(lis):
    """Given a list, possibly nested to any level, return it flattened."""
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


def gen_sequence(l, cur_seq, next_gt):
    # Start by getting list of remaining numbers in the sequence.
    # print(l)
    # print(cur_seq)
    # print(next_gt)
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
    # print(combos)
    bad = ['((','))', '(*', '*)']
    temp = []
    for i in combos:
        # print(i)
        if not any(b in ''.join(i) for b in bad):
            if i[0] != ')' and i[-1]!='(':
                temp.append(list(i))
    # final = [''.join(x) for x in temp]
    return temp

def pattern_seq(seq, pat):
    # ret = ''
    # p = list(pat)
    # s = list(seq)
    for i in range(len(pat)):
        if pat[i] == '(':
            # temp[i] = s[i+1]
            # temp[i+1] = s[i]
            seq[i], seq[i+1] = seq[i+1], seq[i]
    return seq
            
    
def perform_swaps(seqs, pats):
    final = []
    # s = [''.join([str(x) for x in y]) for y in seqs]
    results = {}
    for pat in pats:
        results[''.join(pat)]=[]
        for seq in seqs:
            results[''.join(pat)].append(pattern_seq(seq, pat))
    return results

    
    
says = eval(input("enter an n: "))
results = {}
total_list = []
for i in range(1, says):
    zed = flatten(gen_sequence(list(range(1, says+1)), [i], True))
    results[str(i)] = [x for x in zed if len(x) == says]
    print("\n Alternating sequences starting with %d \n" % i)    
    print(results[str(i)])
    print("\n")
    total_list.extend(results[str(i)])
pats = gen_patterns(says)


print("number of alternating sequences %d \n" % len(total_list))
print("number of swap patterns: %d \n" % len(pats))

performed = perform_swaps(total_list, pats)
outfile = 'output_n_%s.csv' % str(n)
df = pd.DataFrame(performed)
df.to_csv(outfile)

