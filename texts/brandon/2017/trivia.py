# -*- coding: utf-8 -*-

scores_text = """\
exceptions,7
I/0,6
???,4
Stack Overflow trademark violators,7
Closest to the bar!,4
Longhorns,6
__main__,8
"""

def fix(n):
    if not n:
        return u'—'
    return str(n)

if __name__ == '__main__':
    data = []
    for line in scores_text.splitlines():
        fields = [f.strip() for f in line.split('|')]
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
