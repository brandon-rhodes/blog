# -*- coding: utf-8 -*-

from fractions import Fraction as F

# (blank answer sheet for round 1),2.5
# ???,4

scores_text = """\
exceptions,7,6.5,6
1/0,6,7,5.5
Stack Overflow trademark violators,7,7,9 2/3
Closest to the bar!,4,6.5,3 2/3
Longhorns,6,5.5
__main__,8,5.5,10.5
St Python,6,6.5,5
Portland Perl User's Group,5.5,5.5,4 2/3
ssssss,5,5,4 1/6
Perl,5,4,5.5
Major Tom,5.5,4.5,5
Fire Roads,5.5,6.5,5 2/3
RU,3.5,,3 2/3
Not a Dead Parrot,4,5.5,6 1/3
Omegadot and co.,5,5,4 2/3
__struct__,5,7,8.5
pyfecta!!,5,5.5,3 1/3
Bobby Tables,5.5,6,3 2/3
__teamname__,4,6,4.5
The Dunderdogs,4,5.5,4 1/6
EAFP,4,,5.5
Spam & Eggs,5.5,6.5,4.5
"""

def main():
    data = []
    for line in scores_text.splitlines():
        fields = [f.strip() for f in line.split(',')]
        name = fields[0]
        scores = [0 if not s.strip() else to_num(s) for s in fields[1:]]
        scores.extend([0] * (3 - (len(fields) - 1)))
        total = sum(s for s in scores)
        print(total, name)
        data.append((total,) + tuple(scores) + (name,))
    data.sort(reverse=True)
    print('================================== ==== ==== ==== =====')
    print('Trivia Team                           1    2    3 Total')
    print('================================== ==== ==== ==== =====')
    for total, round1, round2, round3, name in data:
        print(('%-34s %4s %4s %4s %5s'
               % (name, fmt(round1), fmt(round2), fmt(round3), fmt(total)))
              # .replace('.0', ' ')
              # .replace('.5', '½')
              # .replace('  —', '— ')
        )
    print('================================== ==== ==== ==== =====')

def to_num(s):
    if s.endswith('.5'):
        n = int(s[:-2])
        return n + F(1,2)
    if '/' in s:
        whole, frac = s.split()
        n = int(whole)
        num, den = frac.split('/')
        return n + F(int(num), int(den))
    return int(s)

def fmt(n):
    if not n:
        return u'—'
    whole, fraction = divmod(n, 1)
    fstr = {
        F(0): ' ',
        F(1,2): '½',
        F(2,3): '⅔',
        F(1,3): '⅓',
        F(1,6): '⅙',
        F(5,6): '⅚',
    }[fraction]
    return '{:2} {}'.format(whole, fstr)

if __name__ == '__main__':
    main()
