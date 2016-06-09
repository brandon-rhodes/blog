---
categories: Computing, Python
date: 2016/06/09 10:50:29
permalink: http://rhodesmill.org/brandon/2016/pycon-trivia/
title: PyCon Trivia Night, Third Edition
---

At PyCon 2016 it was my honor,
for a third year in a row,
to host a Trivia Dinner on the first evening of the conference!
This year’s venue was the storied
`Crystal Ballroom <http://www.mcmenamins.com/CrystalBallroom>`_,
a music venue in Downtown Portland’s west end.
To make sure that our event took full advantage of the big stage,
I booked the `Adventure Capitalists <http://adcap.biz/>`_,
who followed up the trivia dinner
with a rousing set of punk startup tunes:

.. raw:: html

   <blockquote class="twitter-tweet" data-lang="en"><p lang="en" dir="ltr">Have a conference pass? Come by the Crystal Ballroom and see the Adventure Capitalists! <a href="https://t.co/sg0GxqiDpF">pic.twitter.com/sg0GxqiDpF</a></p>&mdash; PyCon (@pycon) <a href="https://twitter.com/pycon/status/737502417797799936">May 31, 2016</a></blockquote>
   <script async src="//platform.twitter.com/widgets.js" charset="utf-8"></script>

Last year’s trivia night questions
focused on such exciting topics as PEP-8 and Python 3,
but it turns out that these were fraught topics
about which most of the audience were not very familiar.
So I made a promise:
the PyCon 2016 trivia night would be all Python 2, all the time!
The questions below dive into and celebrate
the retro roots of the legacy Python language.

With the dinner complete,
I can now reveal the questions and answers!
I will list the questions first,
in case any readers want to tackle them themselves
without the danger of the answers scrolling too quickly into view.
Next, I will list the teams and their scores.
Finally, I will finish with the answers.

----------

First Round Questions
---------------------

0. How do you tell the ``print`` statement not to follow your output
   with a newline?

1. What is the result of running this statement?

   ::

    print >>None, "Hello"

2. How many bytes long is the string that results from typing this into
   Python 2?  ``"\`\'\""``

3. Which of the following Python 2 classes does *not* live in a module
   of exactly the same name? ``Fraction`` ``StringIO`` ``UserDict``

4. A tab character in a line's leading whitespace (in its “indentation”)
   can represent how many individual space characters (specify a range)?

5. What are the two choices of ASCII character that, when appended to a
   numeric constant, turn it into a complex number?

6. Which of these three C implementations was added to Python 2 last?
   ``cPickle`` ``cProfile`` ``cStringIO``

7. What was Python’s first string interpolation mechanism?

8. “Flat is better than” what?

Second Round Questions
----------------------

0. Name at least two languages that inspired the ``>>`` syntax for
   ``print``::

       print >>sys.stderr, "Hello"

1. How many bytes long is the string that results from typing this into
   Python 2? ``'\12345'``

2. What is the name of the keyword argument accepted by the ``list()``
   built-in?

3. Python 2.1 added magic methods for testing equality and inequality.
   What are the names of all six methods?

4. …Their names were borrowed from which other language?

5. What is the result of this Python 2 expression? ::

      2 * `3 * 4`

6. What is the result of this Python 2 expression? ::

      2 * `3 * `4 * 5``

7. Python 2.4 added a new string interpolation mechanism — what is it
   called, and what special character introduces each interpolation?

8. “Although practicality beats” what?

Final Round Questions
---------------------

0. | What writable attribute should your file-like object offer if it
   | wants to fully support Python’s ``print`` statement?

1. How many bytes long is the string that results from typing this into
   Python 2? ``'\a\b\c'``

2. The built-in ``int()`` can take which keyword arguments?

3. Which of the following Python 2 classes does NOT live in a module of
   exactly the same name? ``ConfigParser`` ``Queue`` ``Telnet``

4. The Python 2 Reference Manual uses ‘singleton’ once to refer to the
   ``NotImplemented`` object, and every other time to refer to what
   concept?

5. In Python 2.7, ``sys.version_info`` changed from returning what
   original type to what new type?

6. What was the first-ever ``__future__`` directive?

7. The Python 2.4 release notes describe what new feature as making
   possible, “all sorts of new and shiny evil”?

8. “In the face of ambiguity, refuse the temptation to” what?

----------

The Winning Teams
-----------------

So how did the assembled teams do at tackling these questions?

I am startled to announce a first-ever 3-way tie
between the trivia night winning teams!
Out of a total of 9 × 3 = 27 possible points,
each of the three winning teams scored 17½ total.

============================== ==== ==== ==== =====
Trivia Team                       1    2    3 Total
============================== ==== ==== ==== =====
Palm Dakota Dessert Testers     7    7    3½   17½ 
Site Packages                   6    6    5½   17½ 
The Government                  6    5    6½   17½ 
Bikeshed                        8    5    4    17  
Team Ukraine                    6    6    4½   16½ 
team from down\_\_              5    6½   5    16½ 
wtfj                            6    6    4    16  
Hey Siri, Call Mom              5    7    4    16  
Jessica                         6    5    4    15  
Team Python 4000                5½   6    3½   15  
Portland Satellites             5    4½   5½   15  
AI                              7    5    2½   14½ 
__del__                         5    4    4    13  
Star-args                       7    4    1    12  
Stripper.py                     6    3½   2½   12  
Meowmeow                          —  7    5    12  
Python 3½                       5    5    1½   11½ 
The Python 3 Developers         3    6    2½   11½ 
Just A Flesh Wound              6    2½   2½   11  
team 5/8                        3    3    4½   10½ 
The Dissociative Arrays         6    3    1    10  
import this                     4    4    1½    9½ 
import antigravity              4    4    1     9  
Nevada                          5    3½   0     8½ 
Serpent Trainer                 4      —  2     6  
j.j.w.e.                        5      —    —   5  
PyNoobs                         3    2      —   5  
blue viper                      2    1    0     3  
Pink Panthers                   1    1    1     3  
============================== ==== ==== ==== =====

A dash in the table above indicates a missing answer sheet,
that was either never written
or that did not make it from the team’s table
to my own table up at the front of the venue.

One team,
when they realized that they were not going to be able to answer
a single one of the difficult final-round questions,
decided to offer art instead as their contribution:

.. raw:: html

   <blockquote class="twitter-tweet" data-lang="en"><p lang="en" dir="ltr">One team at PyCon trivia night, finding themselves without a single final-round answer, decided to offer art instead <a href="https://t.co/9oMf3m0RUt">pic.twitter.com/9oMf3m0RUt</a></p>&mdash; Brandon Rhodes (@brandon_rhodes) <a href="https://twitter.com/brandon_rhodes/status/740961349740560385">June 9, 2016</a></blockquote>
   <script async src="//platform.twitter.com/widgets.js" charset="utf-8"></script>

As I could not, of course,
award any points for unsolicited artwork,
I recognized the team’s effort through the above tweet instead.

----------

First Round Answers
-------------------

0. A trailing comma suppresses Python’s usual habit of adding a newline
   at the end of the material that it prints.

1. Printing ``>>None`` prints to ``sys.stdout`` without the
   inconvenience of making you import ``sys`` and name ``stdout``
   directly in your code. This will strike the modern Python programmer
   as needlessly obscure, and a poor trade-off: if a programmer decides
   to use the feature, then almost every other programmer reading the
   code will have to go consult the rules to remember the effect.

2. This question tested knowledge of Python’s string quoting and
   escaping, which it shares with many other languages. Three basic
   rules need to be grasped to answer this question. First: many
   dangerous or unusual characters can be safely typed in a Python
   string constant by preceding them with a backslash — so that the
   single quote in the middle of ``'what\'s up'`` is understood by
   Python to be a simple literal single quote, and not your attempt to
   end the string yet. Second: these rules remain the same whether or
   not the current string’s quoting needs them. There is nothing special
   about a single quote in a double-quoted string, so ``"what's up"`` is
   perfectly safe, but Python likes keeping rules symmetric and so
   ``"what\'s up"`` is allowed too. Third, and most dismayingly: if you
   put a backslash in front of a character that does *not* create a
   recognized backslash code, then instead of giving you an error,
   Python simply assumes you want a backslash in the middle of your
   string. This is C’s behavior, but an example of poor design: most
   users would benefit from an exception of they type an unknown escape
   code, since they can always double up the backslash to make their
   intention clear and be explicit rather than implicit.

   Taking the three elements in ``"\`\'\""`` from right to left:

   * ``\"`` is the simplest case: you want a double-quote in a
     doubly-quoted string, so you escape it, adding a single double
     quote character to your string.

   * ``\'`` is a bit more of a stretch, because the ``\`` is optional:
     you don’t really need it, so what will Python do? As explained
     above, backslash codes work whether the current string needs them
     or not, so this also adds only a single quote character to our
     string.

   * ``\``` is the outlier. Because a backtick is never special or
     dangerous inside a Python string, no matter how it is quoted, the
     language does not bother to define ``\``` as meaning anything. Since
     it is not a recognized escape code, the language assumes you really
     wanted a backslash and backtick: two characters.

   So the resulting string (when written without quotes or escaping,
   since that would confuse things again!) is ``\`'"`` which is 4
   characters long.

3. A bad habit of Python 2 was taking unlike things and giving them
   names with exactly the same spelling — and a particular habit was
   giving modules the name of their most useful class. Both ``StringIO``
   and ``UserDict`` were the names of both a module and also of the
   class that you usually wanted inside. But ``Fraction`` came from the
   ``fractions`` module, differentiating the module name with both case
   and pluralization.

4. According to the Python Reference, a tab character always represents
   at least one space, and adds enough spaces to the line to bring the
   cursor to a position that is a multiple of 8.  It therefore can range
   from meaning 1 space to meaning 8 spaces.

5. I had always thought that ``j`` was the single letter that could turn
   a number like ``4`` into the imaginary number ``4j``, but it turns
   out that the language standard also permits ``4J``.

6. The Python community learned early on that we needed pickling and
   string I/O to happen quickly, but profiling technology matured late
   in the history of Python 2, so ``cProfile`` was the last of the three
   modules added.

7. Famously, Python took the percent-formatting conventions that the
   C language had locked up inside the ``printf()`` and ``sprintf()``
   families of library functions and elevated it to an operator: the
   first Python string interpolation mechanism was ``%`` interpolation.

8. From the Zen of Python, that a Python programmer reads each morning
   before we begin to code: "Flat is better than nested.”

Second Round Answers
--------------------

0. There are many languages that use ``>>`` to direct output to a
   specific file. But according to the BDFL quote in PEP-214, only four
   were known to him as predecessors, and therefore qualify as true
   influences on Python and not simply coincidences: “sh, awk, Perl, and
   C++.”

   https://www.python.org/dev/peps/pep-0214/

1. Bell Laboratories programmers in the early 1970s seem to have found
   it easier to think in octal than in hexadecimal, which makes sense:
   we already come to programming familiar with the numbers 0 through 7,
   while numbers like “B” and “C” can take a long time to get used
   to. (Without stopping to count, can you state their values?) So octal
   was chosen as the base in which difficult-to-type character codes
   could be written, and three octal digits are all that you need to
   specify an 8-bit character: once the language is done reading up to
   three digits following a backslash, it stops and assumes the rest of
   the string is normal. So ``'\12345'`` is a single character ``\123``
   (also known as capital S) followed by the digit ``4`` and the digit
   ``5``. The string ``S45`` has the length 3.

2. This question is all sorts of fun, because the documentation has been
   leading you wrong all of these years. You have probably never used a
   keyword to name the first argument to ``list()``. After all, the
   convention that we can pass an initial value to all built-in types —
   think of calls like ``int('12')`` and ``tuple([3, 4, 5])`` — is so
   pervasive that we never feel the need to be more explicit about the
   purpose of those arguments. But we may have seen a dozen times, when
   running ``pydoc list`` to remember a method name, the keyword
   argument ``iterable`` advertized for the constructor::

       Help on class list in module __builtin__:

       class list(object)
        |  list() -> new empty list
        |  list(iterable) -> new list initialized from iterable's items
        |  ...

   But the documentation is wrong! In the C code of the ``list()``
   initializer, the keyword argument is called ``sequence``, and you can
   verify this by calling it with this keyword argument yourself.

3. The six “rich comparison” method names are::

       __eq__() __ne__() __gt__() __lt__() __ge__() __le__()

   I gave ½ point if a team knew most of them but got one or two wrong,
   and also ½ point if a team knew them all but forgot to put dunders
   around them.

4. While several other languages might also use these abbreviations for
   “greater than,” “less than,” and so on, they all go back to a common
   ancestor: the naming convention comes from Fortran. As PEP-207 says,
   “You gotta love the Fortran heritage.”

5. Okay, this is fun: Python 2 has a special syntax for evaluating an
   expression and turning it into a string!  This is probably the most
   Perl-like feature of Python 2’s syntax, the place where it most
   severely goes off of the rails and uses obscure characters for
   something that could more easily (and readably!) spelled out. Since
   ```3 * 4``` will evaluate to the string ``'12'``, multiplying the result
   by two results in the string ``'1212'``.

6. And this question is even more fun: to answer it, you need to know
   that the *kind* of string generated by putting backticks around an
   expression is not a ``str()`` string, but a ``repr()`` string! So
   after the multiplication by 3 has produced the characters ``202020``,
   the outer pair of backticks go to work by running ``repr()`` which
   slaps a pair of single quotes around those characters. Multiplying
   this by 2 gives the final string (if we write it out without quotes,
   to keep things simple)::

       '202020''202020'

   Oh, and, yes: legacy Python thought its backtick mechanism was so
   important that people would be using backticks *inside* of backticks,
   so the parser is carefully crafted to correctly handle concentric
   backticks. This expression is not, as many of you had fondly hoped, a
   syntax error!

7. Python 2.4, believe it or not, went to the trouble of adding a whole
   new string interpolation mechanism that no one ever uses: the
   ``string.Template`` class! It accepts strings like ``'Hello,
   $name!'`` that use a ``$`` to mark each place that a value should be
   interpolated. Python 2 had a habit of introducing more string
   interpolation mechanisms than the community would actually decide to
   use, and there are hints that Python 3 is making plans to continue
   that tradition.

8. From the copy of the Zen of Python that you keep by your morning
   breakfast cereal: “Although practicality beats purity.”

Final Round Answers
-------------------

0. Your file-like object needs a writable ``softspace`` attribute if a
   ``print`` statement that ends with a comma is going to be able to
   signal to the following ``print`` statement that it needs to precede
   its own material with a space to separate it from the material that
   was already printed.

1. Like the same question in the first round, this tests whether you
   know the backslash escape codes common to the entire family of
   languages that derive their string syntax from the C language. The
   code ``\a`` means the ASCII BEL character (which rang the bell attached
   to old teletypes) and ``\b`` is backspace, so each of those
   two-character escape sequences in the written string represent one
   real character apiece. But ``\c`` does not mean anything special, so it
   remains the two characters backslash and *c*. So the resulting string
   is 4 bytes long.

2. In this case, the docstring shown to you by ``pydoc`` will not have led
   you astray, if you happened to remember it. The second argument has
   the obvious name ``base`` since it lets you specify whether a string
   you have supplied is expected to be in base 8, or base 10, or base 16
   or whatever. The first argument is more obscurely named: the
   initializer specifying the integer’s value is named ``x``. I gave ½
   point if a team knew one but not the other.

3. The ``Telnet`` class lives inside of the ``telnetlib`` module instead of
   simply living inside of a module of the same name as itself.

4. Believe it or not, the Reference Manual for Python 2 consistently
   uses ‘singleton’ as the technical term for a tuple of length one.

5. In Python 2.7, ``sys.version_info()`` stopped returning a plain tuple
   that supported only item access, and started returning a named tuple
   whose elements could also be fetched through attributes like ``.major``
   and ``.minor``. I also gave credit if a team’s answer sheet named the
   specific named-tuple type that gets returned — which just happens to
   be the type ``sys.version_info``!

6. The first-ever ``__future__`` directive was::

        from __future__ import nested_scopes

   Nested scopes were considered dangerous enough that they needed to be
   an opt-in feature for an entire Python version before they became
   official.

7. The powerful language feature introduced in Python 2.4 that was going
   to make possible “all sorts of new and shiny evil” is, startlingly
   enough, the fact that “``eval()`` now accepts any form of object that
   acts as a mapping as its argument for locals.”  Once again, a new
   feature that was apparently expected to open up whole new ways of
   using Python wound up going almost entirely unused — I cannot
   remember once, in even the most magic-ridden Python code, ever having
   seen this superpower taken advantage of.

8. From the copy of the Zen of Python that you re-read on your beach
   vacation as the surf crashes in the background: “In the face of
   ambiguity, refuse the temptation to *guess*.”


