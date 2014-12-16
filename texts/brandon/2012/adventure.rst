---
categories: Python, Computing
date: 2012/04/06 03:02:10
permalink: http://rhodesmill.org/brandon/2012/adventure/
title: Adventure in Python 3
---

I have just released
`adventure 1.2 <http://pypi.python.org/pypi/adventure/1.2/>`_
on the Python Package Index,
an update of my Python 3 port
of the original Colossal Cave Adventure game
that I announced more than a year ago during the final round of
`PyCon 2011 lightning talks <http://pyvideo.org/video/357/pycon-2011--sunday-afternoon-lightning-talks>`_.

.. image:: http://rhodesmill.org/brandon/2012/adventure-heathkit-h19.jpg
   :target: http://www.flickr.com/photos/brandonrhodes/6115627693/

Written in the late 1970s,
“Adventure” was the first game
to offer players a virtual world to explore at their own pace,
driven by their own curiosity.
The player directs the game with simple one- and two-word commands
like ``ENTER`` ``BUILDING`` and ``GET`` ``LAMP``,
together with the cardinal directions —
which can, mercifully, be typed as abbreviations
(``N``, ``NE``, ``E``, ``SE``, and so forth,
with ``U`` and ``D`` for up and down).
Based on a real-life section
of the Flint-Mammoth cave system in Kentucky
that the original author helped map,
“Adventure” invites you to start collecting treasures from the cave
in a quest that eventually involves danger, magic,
and even encounters with a few computer-controlled characters,
who rustle in the darkness beyond the light of your lamp
before finally pouncing.

Keep reading if you want to learn
about several discoveries that I made
while porting “Adventure” to Python!
If you want to know more about the history of the original game itself,
I recommend Dennis G. Jerz's admirably thorough paper
“`Somewhere Nearby is Colossal Cave: Examining Will Crowther's Original ‘Adventure’ in Code and in Kentucky <http://www.digitalhumanities.org/dhq/vol/001/2/000009/000009.html>`_”
from the Summer 2007 issue of the Digital Humanities Quarterly.

Playing at the prompt
---------------------

I was inspired to write the ``adventure`` package
when I realized that typing a name at the Python prompt
could invoke an action if the object it referenced
did something useful inside of its ``__repr__()`` method.

.. more

Recall that a language like Ruby invokes a function
if you merely mention the function's name::

    #!ruby
    jump    # call the "jump" function in Ruby

I imagine that this would make it easy
to implement a game like Adventure at the Ruby prompt.
Typing the name of a command like ``jump`` or ``n`` or ``sw``
would simply invoke it, just like at the prompt of the original game.

In Python, however —
as in higher math more generally,
whose scruples Python tends to honor more faithfully
than do other popular languages —
``jump`` is merely a name,
and its mention merely retrieves a reference to the function it names.
To actually invoke the function you need to follow the name
with a pair of parentheses::

    #!python
    jump()    # call the "jump" function in Python

For more about this distinction,
see the discussion of songs and names-of-songs
between Alice and the Red Knight in
`Chapter VIII <http://en.wikisource.org/wiki/Through_the_Looking-Glass,_and_What_Alice_Found_There/Chapter_VIII>`_
of *Through the Looking Glass*
— remember that Lewis Carroll was a logician in his day job! —
or, if you find his writing too tedious,
start at the Wikipedia article on the
`use-mention distinction <http://en.wikipedia.org/wiki/Use%E2%80%93mention_distinction>`_.
And tell any analytic philosophers you know
that Python is your favorite programming language.

So the following line of Python code by definition does nothing,
except, perhaps — depending on which implementation of Python you use —
innocently incrementing and then decrementing
the ``jump`` object's reference count::

    #!python
    jump    # fetches then discards a reference

But things are quite different if,
instead of appearing in a script on a line by itself,
the bare name is typed at the interactive Python prompt.
The third action taken by the prompt's read-eval-print loop —
the “print” action —
invokes the object's ``__repr__()`` method.
A normal function simply describes itself::

    #!python
    >>> max
    <built-in function max>

But if we write a class of our own,
we can do arbitrarily complex work when ``__repr__()`` is called! ::

 #!python
 >>> class C(object):
 ...     def __repr__(self):
 ...         print('[advancing the game state]')
 ...         return 'There is a shiny brass lamp nearby.'
 ...
 >>> jump = C()

We now have an object that, when simply named,
causes something to happen and then returns a message
that Python displays to show us the result. ::

 #!python
 >>> jump
 [advancing the game state]
 There is a shiny brass lamp nearby.

And this is what the ``adventure`` package does, in spades.
When you invoke its ``play()`` function at the Python prompt,
it uses the
`inspect <http://docs.python.org/library/inspect.html>`_
Standard Library module
to reach into the scope of your Python prompt
and define every “Adventure” noun and verb as a symbol
whose ``__repr__()`` is sitting ready to be triggered.

The word objects are also supplied with other methods
like ``__call__()`` and ``__getattr__()``
so that words can be composed to form more complex commands,
like ``get(lamp)`` or ``get.lamp`` —
see
`prompt.py <https://bitbucket.org/brandon/adventure/src/86507c6fe2b9/adventure/prompt.py>`_
if you want to read all of the details.

De Morgan and old FORTRAN
-------------------------

The original FORTRAN language
in which “Adventure” is written
does not support “structured programming” —
you cannot combine several statements into a single block of code
under the control of an ``IF`` statement.
Instead, ``IF`` can only govern
the single statement that follows it.
Several statements can be skipped by an ``IF``
only if it does a ``GOTO`` to a line number that follows them.
Here, for example, is an excerpt from ``advent.for``
in which an ``IF`` clause controls two statements,
with normal execution continuing at line ``2630``::

 #!fortran
 2610    IF(WD1.NE.'WEST')GOTO 2630
         IWEST=IWEST+1
         IF(IWEST.EQ.10)CALL RSPEAK(17)
 2630

When I translated this code into Python,
the line number and ``GOTO`` disappeared
in favor of simply indenting the lines that run conditionally::

            #!python
            if word1 == 'west':
                full_wests += 1
                if full_wests == 10:
                    write_message(17)

You will note that my outer Python ``if`` statement
tests a condition that is, in fact, the complete *opposite*
of its equivalent in FORTRAN:
the original code wants the word to not-equal ``'WEST'``
whereas, in my rewrite, I test whether they are equal instead.
The reason is plain enough:
while my modern Python code gets to directly test
whether to *execute* the block of code,
the original FORTRAN has to think backwards
and test whether to *skip* the statements that follow.

(Note that the second ``IF`` statement
controls only a single line of code,
and therefore is written “forwards” even in FORTRAN.)

Flipping a simple ``.NE.`` so that it becomes ``==`` is simple enough.
But what happens when I need to
`reverse the polarity <http://en.wikipedia.org/wiki/Third_Doctor#.22Reverse_the_polarity.22>`_
of a more complex expression? ::

 #!fortran
         IF((WD1.NE.'WATER'.AND.WD1.NE.'OIL')
         1	.OR.(WD2.NE.'PLANT'.AND.WD2.NE.'DOOR'))GOTO 2610
         IF(AT(VOCAB(WD2,1)))WD2='POUR'
 2610

I was delighted!
Here — *finally* — was a use for De Morgan's laws,
a mere seventeen years after I learned them in computer science class.

`De Morgan's laws <http://en.wikipedia.org/wiki/De_Morgan's_laws>`_
state, basically,
that instead of simply slapping ``not`` in front of a large expression —
making your code even harder to read —
you can dive into the big expression and change ``and`` to ``or``,
``or`` to ``and``,
and then reverse the meaning of each equality.
The result will mean precisely the opposite,
the ``not``, of the original big expression.
You do have to be careful with parentheses
since ``and`` and ``or`` have different precedence
in most programming languages,
but De Morgan let me convert the FORTRAN above
into roughly this Python translation::

        #!python
        if ((word1 == 'water' or word1 == 'oil') and
            (word2 == 'plant' or word2 == 'door') and
            self.is_here(self.referent(word2))):
            ...

And the result works great.
In general, much of the work
of translating “Adventure” to Python
involved taking FORTRAN code that said one thing
and making it say more or less exactly the opposite,
so that I could replace ``GOTO`` statements
with more modern — and more readable — control flow.

Testing randomness is tricky
----------------------------

The main tests for the game are two large walkthroughs.
You can find them in the package's ``tests`` directory.
Since the game is playable at the Python prompt,
each walkthrough is simply a long docfile
that starts the game and plays to completion.
I pass them to a Standard Library
`DocFileSuite <http://docs.python.org/library/doctest.html#doctest.DocFileSuite>`_
and away they go.

As soon as I started implementing game elements
that involved chance, my tests started breaking,
because the series of numbers from the
`random <http://docs.python.org/library/random.html>`_
Standard Library module is different every time you run Python.
This has a well-known fix:
at the beginning of each test
I set the ``random`` generator's seed value,
making the sequence of pseudo-random numbers
unfold in the same order every time.
In case anyone runs my tests in parallel,
I even abandoned the global random number generator
and gave each instance of my ``Game`` class
its own ``Random()`` object,
so that two games going at once
will not interfere with each other's stream of random numbers.
So each walkthrough starts with something like::

 >>> import adventure
 >>> adventure.play(seed=2)
 WELCOME TO ADVENTURE!!  WOULD YOU LIKE INSTRUCTIONS?
 <BLANKLINE>
 >>> no

After all of that caution, I felt betrayed and dismayed
when the tests *still* wound up being random,
giving different output every time they were run!

It took me quite a long time to realize
that my problem was this scrap of code::

    #!python
    locations = {
        # every Room() object reachable from here
        }
    next_room = self.random.choice(locations)

Why is this code a problem?
Because of four different facts
that, when combined together, make trouble:

* To choose an item from a set ``s``,
  ``choice()`` selects an integer ``0`` ``≤`` ``n`` ``<`` ``len(s)``
  and iterates over ``n`` items to find item number ``n``.

* Sets, by definition, they have no inherent ordering.

* When faced with quite generic objects like my ``Room`` instances,
  Python sets must hash and store them by their memory addresses.

* Finally, Python object memory address are not stable
  from one run of the interpreter to the next,
  even if you are running exactly the same sequence of operations!

So the random number generator
would indeed return a stable value like, say, 3,
but iterating across ``locations`` would yield a different
“object 3” each time I ran my tests.

The worse part was that these random room decisions were hidden —
their consequences were not immediately visible to the player —
so the walkthrough would not fail until much later,
when the execution of the above code snippet was far in the past.
I kept staring at the code at the point of failure,
not at all suspecting that the random number generator
was being knocked off course invisibly
a hundred lines earlier in the walkthrough!

The solution was simple: to sort the rooms into a list
on some criteria *other* than their memory address
before letting ``choice()`` get to work on them.

A grand adventure, at 1200 baud
-------------------------------

My final discovery was made quite by accident.
Now that “Adventure” could be played at the Python prompt,
I also added a real console prompt that requires no syntactic magic.
Simply invoke the ``adventure`` package and start typing::

    $ python -m adventure
    WELCOME TO ADVENTURE!!  WOULD YOU LIKE INSTRUCTIONS?

    > no
    YOU ARE STANDING AT THE END OF A ROAD BEFORE A SMALL BRICK BUILDING.
    AROUND YOU IS A FOREST.  A SMALL STREAM FLOWS OUT OF THE BUILDING AND
    DOWN A GULLY.

    > enter building

Just for fun, I replaced the ``print`` statement with a delayed loop
that prints characters at the speed of a 1200 baud modem
like the modem over which I myself first played the “Adventure” game.
And after a few minutes of playing
I was suddenly brought up short
by the fact that the game seemed, somehow, to be more fun
when the text was presented slowly.

What was going on?

I paid close attention to the game experience,
and remembered that the human eye scans — and does not merely read —
a block of text that appears on the screen all at once.
Even if you intend to read a paragraph as narrative,
your eyes will jealously dart forward
to get a glimpse of what happens next;
your mind wants to initially take in the paragraph as *gestalt*.
Recall how hard it is to pay attention in a novel,
if farther down the page you see emphatic lettering
that signals that something terrible is about to happen!

Now consider the following event
from early in the “Adventure” game::

 > n
 YOU ARE IN THE HALL OF THE MOUNTAIN KING, WITH PASSAGES OFF IN ALL
 DIRECTIONS.

 A HUGE GREEN FIERCE SNAKE BARS THE WAY!

When this text is presented all at once,
my eye jumps immediately to the exclamation point,
finds out about the snake,
and only then — almost as an afterthought — gets around to reading
about my location.
It only makes things worse that the news about the snake
will have appeared nearly on top
of where my prompt was sitting
as I watched myself type the ``s`` command.

It would normally be exciting to reach a location
with as storied a name as “the Hall of the Mountain King.”
Both Ibsen and Tolkien might leap to mind.
And after the safety of exploring narrow corridors,
a shiver goes down my spine to realize that my lamp
no longer finds solid walls close at hand,
but that passages recede into darkness in “all directions.”
All of this can be ruined if I read first about the snake
and hardly pause to read the room description
because I am thinking about my safety instead.

At 1200 baud my experience of the text is completely different.
It does scroll by at a speed faster than I can read —
I am not bored waiting for more text to appear as I am at 300 baud —
but I am forced, as were all early “Adventure” players,
to learn something about my location
before I am then startled by the presence of danger.
And the danger feels all the more acute
if I know already that this is the Hall of the Mountain King which,
offering passages in all directions,
lacks even a single wall that I could turn my back against.

I am happy to have solved the technical puzzle
of how “Adventure” might be played at the Python prompt.
And without the challenge
it would not have occurred to me to sit down over Christmas 2010
and to start porting the game in the first place.
But having played the game both ways —
with descriptions appearing instantly at the Python prompt,
versus being printed slowly by a dedicated game prompt —
I must say that I much prefer the latter.

And so I suggest,
if you are playing “Adventure” for the first time,
that you invoke it with ``-m``
and simply ignore the fun that I had as I conquered
the limitations of the Python prompt.
You and the game deserve it!
