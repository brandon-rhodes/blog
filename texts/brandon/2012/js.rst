---
categories: Computing, Python
date: 2012/01/15 02:59:10
permalink: http://rhodesmill.org/brandon/2012/js/
tags: ''
title: JavaScript Breaks Math
add_mathjax: True
---

Why do we Python programmers
stay so annoyed with JavaScript's broken ``this`` keyword?
After all, every programming language has rough edges.
The problem with ``this`` even turns out to be easy to work around
once you learn the knack.
So why does it feel like JavaScript has committed a fresh offense
every time we trip over it?

The answer, I suggest, is that JavaScript manages to disturb
very deep mental scaffolds
with the behavior of the ``this`` keyword.
Not all programming language annoyances are created equal.
Some involve inconsistency within a language itself,
when a pattern set up by one feature is broken by another
(think of method names in the Python Standard Library).
More serious issues can involve hassles with a language's syntax
or poor behaviors within its type system.
But in this case JavaScript decided
that it would abandon a key property
of the system that lies *beneath* it —
that it would break the conventions that,
in fact, underlie all programming languages.

JavaScript decided that it would break *mathematics.*

Let me explain by starting with a simple example.
You are already familiar with operator precedence,
and how multiplication binds more tightly than
addition when both operators appear in the same expression.
In the following expression,
*a* will first be multiplied with *b*,
then the result of that operation will be added to *c*.

| (1)
| *n* = *a* × *b* + *c*

There is, in other words,
a hidden intermediate result inside of this equation:
the result of the multiplication.
So (1) is, in fact, a shorthand
for writing this sequence of two separate binary operations:

| (2)
| *x* = *a* × *b*
| *n* = *x* + *c*

Note that our ability to transform (1) into the pair of lines (2)
does not involve any special properties of the operators themselves.
This does *not* illustrate some special feature
of multiplication or addition,
like the Distributive Property!
Instead, we are working down at the lower and more fundamental level
of asking what a complex math expression even *means*.
So while we must use argument and proof
to learn that addition is commutative,
the operators and their precedence are simply
a matter of *definition* —
of what we decide it means when we string symbols together
to form an expression in the first place.

Now it turns out that the familiar programming language idiom
of calling a method in a language like Python or JavaScript
is quite precisely analogous to expression (1),
because it separates three symbols
with a pair of binary operators,
where the left operator binds most tightly::

    #!python
    (3)   n = a.b(c)

Until a programmer really grasps what it means
for a language to have “first-class functions” —
functions that can themselves be manipulated as values —
it might be difficult to see that ``a.b``
makes quite good sense simply standing by itself.
It means “take the ``a`` object,
look and see whether it has an attribute named ``b``,
and resolve the value of that attribute.”
And so ``a.b`` works perfectly in front of ``(c)``
so long as the result of the attribute lookup
happens to return a callable.

So expression (3) can be decomposed like expression (1),
and in Python the following two steps are
exactly equivalent to statement (3) —
except, of course, for defining an extra local variable ``fn``::

    #!python
    (4)    fn = a.b
           n = fn(c)

This is, again, simply a property of how expressions work in math —
of the fact that you ought to be able to compute intermediate results
by pulling an expression apart into its constituent binary operations.
But, alas, JavaScript decided to break this property of expressions,
and makes extra invisible magic happen
when the two operators are used in combination —
magic that does not happen when they are separated into separate steps.
Or, perhaps there is a more interesting way to think about it::

    #!js
    /* In JavaScript this is NOT a pair of binary operations. It is a SINGLE
       ternary operator that, to sow confusion among programmers, happens to
       use the same symbols as two well-known binary operations. */

    a.b(c);

    /* This ternary operator is roughly equivalent to: */

    var fn = a.b;
    var old_this = this;
    this = a;
    fn(c);
    this = old_this;

Younger programmers,
for whom ``a.b(c)`` is simply a gesture,
may find our distaste for JavaScript's behavior inexplicable.
The problem is worst
for the experienced programmer or mathematician,
who — every time she types it —
remembers what the dot and parentheses really mean
as clean and separate operations,
but has to remember that their meanings change
when they appear in combination.
This semantic instability flaunts a very long tradition
of defining math operators
so that expressions can be composed together
and broken down again
without changing their meaning.

And that, I think, is why it annoys us:
because from early grade school through college
we have learned that math expressions compose and decompose cleanly,
and JavaScript takes that symmetry away.

One last note for newer Python programmers reading this:
you might be suspecting that Python itself has some kind of magic
involved here, because how else could it remember later
whether you had pulled method ``fn``
off of the specific object ``a``
instead of off some other instance of that class?
The answer is that every lookup of an instance method
returns a new object, called a *bound method*,
that remembers the object on which the lookup took place.

>>> class C:
...     def __init__(self, n):
...         self.n = n
...     def __repr__(self):
...         return 'C%d' % self.n
...     def fn(self, m):
...         return self.n + m
... 
>>> a = C(100)
>>> b = C(220)
>>> a.fn
<bound method C.fn of C100>
>>> b.fn
<bound method C.fn of C220>
>>> b.fn(5)
225

What about your own least favorite language features,
whether in JavaScript, Python, or something else?
Are they all simply about scruples and inconvenience?
Or can you identify some deep-seated assumptions
of your own mental scaffolding
that keep ruining your experience with a specific language?
Let us know in the comments!
