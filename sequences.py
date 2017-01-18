import itertools

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
    combos = list(itertools.combinations_with_replacement(l, n))
    print(combos)
    bad = ['((','))', '(*', '*)']
    temp = []
    for i in combos:
        print(i)
        if not any(b in ''.join(i) for b in bad):
            temp.append(i)
    print(temp)
            
            
        
    # z = [x for x in combos if '((' not in ''.join(x)]
    # y = [x for x in z if '))' not in ''.join(x)]
    # v = [x for x in y if '*)' not in ''.join(x)]
    # u = [x for x in v if '(*' not in ''.join(x)]
    # front = [x for x in u if x[0]!=')']
    # back = [x for x in front if x[-1]!='(']



says = eval(input("enter an n: "))
results = {}
for i in range(1, says):
    zed = flatten(gen_sequence(list(range(1, says+1)), [i], True))
    results[str(i)] = [x for x in zed if len(x) == says]
    print("\n %d \n" % i)    
    print(results[str(i)])
gen_patterns(says)
