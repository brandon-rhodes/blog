# -*- coding: utf-8 -*-

scores_text = """\
(blank),2.5
???,4
exceptions,7,6.5,6
1/0,6,7,5.5
Stack Overflow trademark violators,7,7,9.67
CPosest to the bar!,4,,3 2/3
Longhorns,6,5.5
__main__,8,,10.5
St Python,6,,5
Portland Perl User's Group,5.5,,4 2/3
ssssss,5,,4.167
Perl,5,4,5.5
Major Tom,5.5,,5
Fire Roads,5.5,6.5,5 2/3
RU,3.5,,3.67
Not a Dead Parrot,4,5.5,6.33
Omega dot and co.,5,5,4.67
__struct__,5,7,8.5
pyfecta!!,5,,3 1/3
Bobby Tables,5.5,3.67
__teamname__,4,6,4.5
The Dunderdogs,4,5.5,4.167
EAFP,4,,5.5
Spam & Eggs,5.5,6.5,4.5
"""

def fix(n):
    if not n:
        return u'—'
    return str(n)

if __name__ == '__main__':
    data = []
    for line in scores_text.splitlines():
        fields = [f.strip() for f in line.split(',')]
        name = fields[0]
        scores = [0 if not s.strip() else float(s) for s in fields[1:]]
        scores.extend([0] * (3 - (len(fields) - 1)))
        total = sum(s for s in scores)
        print(total, name)
        data.append((total,) + tuple(scores) + (name,))
    data.sort(reverse=True)
    print('================================== === === === =====')
    print('Trivia Team                          1   2   3 Total')
    print('================================== === === === =====')
    for total, round1, round2, round3, name in data:
        print(('%-34s %4s %4s %4s %5s'
               % (name, fix(round1), fix(round2), fix(round3), total))
              .replace('.0', ' ')
              .replace('.5', '½')
              .replace('  —', '— ')
        )
    print('================================== === === === =====')
