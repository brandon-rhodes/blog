# -*- coding: utf-8 -*-

# Recognizing the three score sheets:
# Round 1  "ascii  bytearray  exec"
# Round 2  "apply  combine  file"
# Round 3  "zlib  tarfile  hashlib"

scores_text = """\
Accidental Combustion | 7 | 8 | 3.5
Badgers | 7 | 7 | 3
Brandon Rhodes’s Team | 8 | 5 | 4
Data, the gathering | | 3 | 3.5
Cache Invalidation | 7 | 8 | 3.5
__dogs__ | 8 | 9 | 5.5
from answers import * | 4 | 6 | 4.5
Give Us Free Drinks On The House | 6 | 5 | 3.5
Import Antigravity | 9 | 11 | 7.5
JSON & the kwargonauts | 9 | 9 | 4
**kwargs | 7 | 5 | 4.5
Literally LVH | 8 | 6 | 3
raise NameError | 4 | 5 | 5.5
Team PHP | 8 | 4 | 7
Team Spam, Spam, and Spam | 6 | 6 | 5
The Holy Hand Grenade of Antioch | 8 | 5 | 3.5
The Ran Vossums | 7 | 5 | 4.5
Unless You’re Dutch | 9 | 7 | 5.5
U+1F40D | 5 | 8 | 3.5
Why is the rum always gone? WHY!? | 5 | 2 | 2
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
