---
categories: Computing, Python
date: 2015/04/16 12:00:00
permalink: http://rhodesmill.org/brandon/2015/pycon-trivia/
title: PyCon Trivia Night, Second Edition
---

As was the case
during first year that the conference was in Montréal,
I was invited for PyCon 2015 to lead an evening dinner trivia contest
on the first full conference day.

Wanting to help the audience celebrate
all of the advances that are being made in Python 3,
I skewed my questions heavily in the direction
of the strides that the core developers are taking
with the new version of the language.
Alas!
My focus was not as popular with the audience
as I had hoped.
It turns out that Python 2.7 is still far more popular
than its predecessor,
and many contestants were frustrated
about being asked so many questions and details
about a language hardly anybody used.
So I made a promise to the audience:
if a third trivia dinner happens at PyCon 2016 in Portland,
that I will make it Retro Python Trivia Night
and ask all of the questions about the Python 2 series!

The questions follow,
then the answers are way down at the bottom of the post
so you can try answering on your own
before you scroll down and peek.
Enjoy!

----------

First Round Questions
---------------------

0. To open a URL in the user’s
   default browser, you would use
   which Standard Library module?

1. In Python 3, an integer
   with a leading ``0`` is
   now a syntax error.
   How do you write the old value
   ``0123`` in modern Python 3?

2. What does the optional second
   argument to ``sum()`` do?

3. What does the optional final
   argument to ``slice()`` do?

4. For or against?
   Is PEP-8 for or against
   this code’s formatting?

::

 def complex(real, imag = 0.0):

5. For or against?
   Is PEP-8 for or against
   this code’s formatting?

::

 if (this_is_one_thing
         and that_is_another_thing):
     do_something()

6. Which is NOT a built-in
   that was newly added
   in Python 3?
   ``ascii()``
   ``bytearray()``
   ``exec()``

7. The ``a[b]`` operation,
   backed by the method ``__getitem__()``,
   is supported by both ``list`` and ``dict``.
   But a ``list`` raises ``IndexError``
   while a ``dict`` raises ``KeyError``.
   What is the most *specific* Python
   exception you can catch that covers both
   ``IndexError`` and ``KeyError``?

8. What do the letters ``gai``
   stand for in the Standard
   Library’s ``gaierror?``

9. “A Foolish Consistency
   is the *(what?)* of Little Minds”

Second Round Questions
----------------------

0. Which Standard Library module
   does *not* parse command line arguments
   when invoked with the ``-m`` option?

   a. ``json``
   b. ``webbrowser``
   c. ``uu``

1. The functions in the ``uuid`` module
   run from ``uuid1()`` through what?
   (BONUS: Which number is skipped?)

2. What does the optional third
   argument to ``getattr()`` do?

3. What does the optional third
   argument to ``pow()`` do?

4. For or against?
   Is PEP-8 for or against
   this line of code?

::

 hypot2 = x * x + y * y

5. For or against?
   Is PEP-8 for or against
   this code’s formatting?

::

 def munge(sep: AnyStr = None):

6. Which one of these three
   is **NOT** a built-in that was
   removed in Python 3?
   ``apply()``
   ``compile()``
   ``file()``

7. PEP-8 recommends that lines of code
   have, at most, how many characters?

8. What does the letter ``h``
   stand for in the Standard
   Library’s ``herror?``

9. Special cases aren’t
   special enough to *_*?

Third Round Questions
---------------------

0. In Python 3.4, which Standard Library
   module now parses command line
   options if invoked with ``python`` ``-m``?

   a. ``zlib``
   b. ``tarfile``
   c. ``hashlib``

1. What happens if you run ``python -m turtle``?

2. ``import sys; delattr(sys, 'getrefcount')``
   What is the result?

   a. ``TypeError``
   b. ``AttributeError``
   c. ``sys.getrefcount()`` disappears
   d. ``sys.getrefcount()`` remains

3. What does the optional final
   argument to ``property()`` do?

4. For or against?
   Is PEP-8 for or against
   this line of code?

::

 c = (a + b) * (a - b)

5. When writing English comments,
   PEP-8 recommends *what?*

   a. *Chicago Manual of Style*
   b. *The Elements of Style*
   c. *Associated Press Stylebook*
   d. Always ending with a period

6. In Python 3, which of the
   following expressions will throw
   an exception (choose all that apply)?

   a. ``bytearray(memoryview(bytes()))``
   b. ``bytes(bytearray(memoryview()))``
   c. ``memoryview(bytes(bytearray()))``

7. PEP-8 recommends that lines
   with comments or docstrings have,
   at most, how many characters?

8. In Python 3.3, which
   did **NOT** become a
   synonym of ``OSError?``
   ``EnvironmentError`` ``WindowsError`` ``VMSError``

9. Namespaces are *what?*

----------

The Winning Teams
-----------------

The teams with the highest scores are sorted at the top
— congratulations, everyone!

================================== === === === =====
Trivia Team                          1   2   3 Total
================================== === === === =====
Import Antigravity                  9  11   7½  27½
__dogs__                            8   9   5½  22½
JSON & the kwargonauts              9   9   4   22 
Unless You're Dutch                 9   7   5½  21½
Team PHP                            8   4   7   19 
Cache Invalidation                  7   8   3½  18½
Accidental Combustion               7   8   3½  18½
Literally LVH                       8   6   3   17 
Brandon Rhodes's Team               8   5   4   17 
Badgers                             7   7   3   17 
Team Spam, Spam, and Spam           6   6   5   17 
The Holy Hand Grenade of Antioch    8   5   3½  16½
The Ran Vossums                     7   5   4½  16½
\*\*kwargs                          7   5   4½  16½
U+1F40D                             5   8   3½  16½
Give Us Free Drinks On The House    6   5   3½  14½
from answers import \*              4   6   4½  14½
raise NameError                     4   5   5½  14½
Why is the rum always gone? WHY!?   5   2   2    9 
Data, the gathering                 —   3   3½   6½
================================== === === === =====

A dash in the table above indicates a missing answer sheet,
that was either never written
or that did not make it from the team’s table
to my own table up at the front of the venue.

----------

First Round Answers
-------------------

0. ``webbrowser``

1. Two possible answers are ``83`` or ``0o123``.

2. Provide the initial value,
   which is also the default returned
   if the sequence is empty.

3. The final argument to ``slice()`` provides the step increment
   that will be the difference between successive values
   in the returned sequence.

4. PEP-8 is against ``complex(real, imag = 0.0)``
   because the ``=`` attaching a default value to a keyword argument
   should not have spaces around it.

5. PEP-8 is in favor of extra indentation
   to visually distinguish extra lines of an ``if`` condition
   from the 4-space-indented code that follows.

6. ``bytearray()`` already exists in Python 2.

7. ``LookupError`` is the superclass of ``IndexError`` and ``KeyError``.

8. It means “getaddrinfo() error.”

9. “A Foolish Consistency is the *Hobgoblin* of Little Minds” —
   the title of the first major section of PEP-8
   after its Introduction.

Second Round Answers
--------------------

0. The ``json`` module cannot be invoked as a command.

1. The highest numbered UUID function is ``uuid5()``,
   and ``uuid2`` is the one which is skipped and does not exist.

2. The third argument to ``getattr(obj, name, x)``
   is the default returned if not attribute of that name exists.

3. The third argument to ``pow()`` provides the modulo
   that should be applied to the return value.

4. PEP-8 is against the formatting of ``x * x + y * y``
   because there is no visual hint indicating
   that multiplication binds more tightly than addition.

5. PEP-8 likes how ``def munge(sep: AnyStr = None):``
   puts spaces between the annotation type and the argument’s default
   value.

6. Python 3 elected not to remove the ``compile()`` builtin.

7. PEP-8 recommends 79 or 99 characters per line,
   depending on how generously one reads it,
   so both answers were considered correct for the trivia scoring.

8. An ``herror`` is a “host error” from the networking code.

9. “Special cases aren't special enough to *break the rules.”*

Third Round Answers
-------------------

0. Python 3 gave a command line interface to the ``tarfile`` module.

1. A graphical turtle demo starts running,
   show the kinds of drawing primitives and patterns it supports.

2. **c** — true to Python’s mutable nature,
   there is no law against removing this attribute
   or, in general, against removing things from ``sys``.
   Run ``del`` and the function disappears.

3. The final (optional) argument to ``property()``
   provides the property’s docstring.
   I had always thought it provided the deleter,
   but there was another argument after that I hadn’t know about!

4. PEP-8 is, amazingly enough —
   and the trivia crowd protested out loud when I announced it —
   *against* the formatting of ``c = (a + b) * (a - b)``
   because it wants less whitespace around more tightly
   binding operations even if parentheses are present.

5. PEP-8 recommends that *The Elements of Style*
   guide the English used in Python comments.

6. The expression ``bytes(bytearray(memoryview()))``
   because ``memoryview()`` cannot be called with no arguments —
   a memory view must be a view of some other value.

7. Comments and docstrings are limited to 72 characters by PEP-8.

8. ``VMSError``

9. From PEP-20, the Zen of Python:
   “Namespaces are one honking great idea -- let's do more of those!”
