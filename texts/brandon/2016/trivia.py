# -*- coding: utf-8 -*-

scores_text = """\
wtfj | 6 | 6 | 4
Team Python 4000 | 5.5 | 6 | 3.5
Palm Dakota Dessert Testers | 7 | 7 | 3.5
The Python 3 Developers | 3 | 6 | 2.5
Just A Flesh Wound | 6 | 2.5 | 2.5
Stripper.py | 6 | 3.5 | 2.5
AI | 7 | 5 | 2.5
Serpent Trainer | 4 | x | 2
Bikeshed | 8 | 5 | 4
Jessica | 6 | 5 | 4
Hey Siri, Call Mom | 5 | 7 | 4
__del__ | 5 | 4 | 4
The Government | 6 | 5 | 6.5
Site Packages | 6 | 6 | 5.5
Portland Satellites | 5 | 4.5 | 5.5
Meowmeow | x | 7 | 5
team from down__ | 5 | 6.5 | 5
team 5/8 | 3 | 3 | 4.5
Team Ukraine | 6 | 6 | 4.5
Star-args | 7 | 4 | 1
blue viper | 2 | 1 | 0
import this | 4 | 4 | 1.5
Python 3.5 | 5 | 5 | 1.5
import antigravity | 4 | 4 | 1
Pink Panthers | 1 | 1 | 1
The Dissociative Arrays | 6 | 3 | 1
Nevada | 5 | 3.5 | 0
PyNoobs | 3 | 2 | x
j.j.w.e. | 5 | x | x
"""

def fix(n):
    if n is None:
        return u'—'
    return str(n)

if __name__ == '__main__':
    data = []
    for line in scores_text.splitlines():
        fields = [f.strip() for f in line.split('|')]
        name = fields[0]
        scores = [None if s == 'x' else float(s) for s in fields[1:]]
        total = sum(s for s in scores if s is not None)
        data.append((total,) + tuple(scores) + (name,))
    data.sort(reverse=True)
    print('============================== ==== ==== ==== =====')
    print('Trivia Team                       1    2    3 Total')
    print('============================== ==== ==== ==== =====')
    for total, round1, round2, round3, name in data:
        print('%-30s %4s %4s %4s %5s'
              % (name, fix(round1), fix(round2), fix(round3), total))
    print('============================== ==== ==== ==== =====')
