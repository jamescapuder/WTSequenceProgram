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
    combos = list(itertools.product([')', '(','*'], repeat=n))
    # print(combos)
    bad = ['((','))', '(*', '*)']
    temp = []
    for i in combos:
        # print(i)
        if not any(b in ''.join(i) for b in bad):
            if i[0] != ')' and i[-1]!='(':
                temp.append(i)
    final = [''.join(x) for x in temp]
    return final
    #print(final)
            
            
        
    # z = [x for x in combos if '((' not in ''.join(x)]
    # y = [x for x in z if '))' not in ''.join(x)]
    # v = [x for x in y if '*)' not in ''.join(x)]
    # u = [x for x in v if '(*' not in ''.join(x)]
    # front = [x for x in u if x[0]!=')']
    # back = [x for x in front if x[-1]!='(']


def pattern_seq(seq, pat):
    # ret = ''
    p = list(pat)
    s = list(seq)
    for i in range(len(p)):
        if pat[i] == '(':
            # temp[i] = s[i+1]
            # temp[i+1] = s[i]
            s[i], s[i+1] = s[i+1], s[i]
    return ''.join(''.join([str(x) for x in s]))
            
    
def perform_swaps(seqs, pats):
    final = []
    s = [''.join([str(x) for x in y]) for y in seqs]
    for c in s:  # each sequence
        # print("\n sequence: %s" % c)
        for p in pats:
            # print("\n pattern: %s" % p)
            swapped = pattern_seq(c, p)
            # print("\n swapped: %s" % swapped)
            if swapped in s:
                final.append((c, p, swapped))
    return final

    
    
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
pattern_dict = {}
for i in pats:
    pattern_dict[i] = [x for x in performed if x[1] == i]
    print("%s: %s copies\n\t%s" % (i, str(len(pattern_dict[i])),'\n\t'.join([x[0] for x in pattern_dict[i]])))
