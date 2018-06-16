
# Learning SymPy while eliminating trigonometry from rotations

I have played with Python’s
[SimPy symbolic math library](http://simpy.readthedocs.io/en/latest/) before,
but for the first time last week I used it to solve a real problem!
In the process I had to confront three errors
in my understanding of how SymPy works:

1. I had somehow imagined that SymPy was secretly storing
   all the equations I was writing
   and would use them automatically later.
2. I thought I could convince SymPy to eliminate intermediate symbols.
3. I thought each variable in my problem needed to be a SymPy symbol.

While working through these misunderstandings to a solution,
I ran across two features that made SymPy’s results
easier to use in my Python code than I had expected!

1. SymPy not only supports fancy formatting of math formulae,
   but can print them as pure Python expressions
   ready to be pasted into a Python program.
2. SymPy can perform subexpression elimination
   to prevent your code
   from computing any sub-result twice.

The sections of this post tackle each of the items above in turn.<!--more-->

## Why did I wind up enlisting SymPy?

The gradual elaboration of my
[Python astronomy library Skyfield](http://rhodesmill.org/skyfield/)
has now reached the verge of producing star charts.
To produce a chart,
the unit vectors for the sky full of stars
need to be rotated
so that the center of the chart
winds up pointing along one of the coordinate system’s axes.

The naive approach requires two fraught crossings
of the boundary
between the clean and confident realm of Cartesian coordinates
and the more troubled realm of spherical coordinates.
Given the position $(x, y, z)$ of the star one wants
at the center of the chart,
the first step is determining its spherical longitude and latitude —
the angle $\phi$ of the vector around the $xy$ plane
and its angle $\theta$ above or below the $xy$ plane:

$$ \eqalign{ \phi &= \tan^{-1}(y, x) \cr \theta &= \sin^{-1}(z) } $$

These two angles are then used to build two matrices.
The first rotates any star $-\phi$ around the $z$-axis.

    %pylab inline
    from sympy import *
    init_printing(use_latex='mathjax')
    π = pi
    x, y, z, xi, yi, zi, xo, yo, zo, 𝜃, 𝜙 = symbols(
        r'x y z x_i y_i z_i x_o y_o z_o \theta \phi'
    )

    rot_axis3(-𝜙)

The second rotates it up towards the $+z$ axis.

    rot_axis2(π/2-𝜃)

Given an input star's position vector $x_i, y_i, z_i$,
the result of multiplication by these matrices
will be an output vector $x_o, y_o, z_o$
where the stars that were originally grouped around the target star in the sky
will now be neatly grouped about the top of the $+z$ axis
and are ready for projection on to the flat surface of a star chart.

## Here be dragons

But it’s inelegant to implement the above formulae directly,
because they involve a sharp descent
from the bright heights of Cartesian coordinates
into the dim sublunary world of spherical coordinates.

The brilliance of Cartesian coordinates
is the admirable symmetry
with which they freight their coordinates with significance.
Whatever the values of $x$ and $y$, for example,
an adjustment $\epsilon$ to $z$
will move the tip of the vector by the exact same amount —
whether the vector's length is a mere kilometer
or a parsec.

By contrast,
the significance of the spherical angle $\phi$
around the equator varies wildly.
Its effect is greatest
when the vector points along the sphere’s equator,
but drops all the way to zero —
it becomes meaningless
and its floating-point precision is _completely squandered_ —
when the vector points at one of the poles.

And trigonometric functions themselves involve numerous subtleties
when implemented in floating point arithmetic on a computer.
I’m indebted to Skyfield contributor
[Josh Paterson](https://github.com/JoshPaterson)
for bringing to my attention
William Kahan’s work on floating point precision
— see, for example, §12 “Mangled Angles”
of his paper
[How Futile are Mindless Assessments of Roundoff
in Floating-Point Computation](https://people.eecs.berkeley.edu/~wkahan/Mindless.pdf).

But I knew there was a way out.
Since the angles $\theta$ and $\phi$
are in this case derived from $x, y, z$ coordinates in the first place,
it should be possible to express the output vector
in terms of the inputs
using no trigonometry at all —
the angles can disappear entirely!

But I wasn’t eager to perform all the substitutions by hand,
so I turned to Python’s `SymPy` library.

## First mistake: thinking there was global state

While I know that well-written software
avoids maintaining global state,
SymPy was so similar to older systems I had experience with —
particularly Mathematica —
that as I typed each formula
I repeatedly imagined
that I was feeding knowledge into a central SymPy data store
from which it would draw conclusions.

But that's simply not how SymPy works.
When you say something like:

    Eq(y, z - 2)

— you are not enrolling this fact in a magical SymPy data store,
and SymPy will not remember the equation later
when you then ask it to solve for something:

    solve(y, z)

The `solve()` routine here found no solutions,
because it doesn’t remember that I typed the earlier equation —
`solve()` is, in fact, a true function:
it knows only the information you provide as arguments.
The equation object needs to be provided
as one of the arguments to `solve()`:

    solve(Eq(y, z - 2), z)

It also did not help —
as I labored under the delusion
that I was slowly feeding new facts into SymPy —
that each time I should have written `Eq(a, b + 2)`
I instead tended to write `a = b + 2`
which, per the usual rules of Python assignment,
destroys the symbol `a` and replaces it with an expression object.
I suppose I should have been more careful
to actually read Sympy’s documentation straight through,
instead of dipping in to sample it —
especially given the fact that SymPy is a project whose
[Tutorial](http://docs.sympy.org/latest/tutorial/index.html)
ominously puts the section “Gotchas” _ahead_ of the section “Basic Operations”!

## Second mistake: I though I could convince SymPy to eliminate variables

I prefer thinking about trigonometry in the "forwards" direction:

$$ z = sin(\theta) $$

It always feels backwards for the human,
rather than the machine,
to be in charge of flipping the equation around
to unnatural arc-trigonometry:

$$ \theta = sin^{-1}(z) $$

SymPy was indeed willing to invert the trigonometry
when only two variables were involved:

    solve(Eq(z, sin(𝜃)), 𝜃)

The problem is that I never figured out how to ask SymPy
to eliminate intermediate variables that I wasn’t interested in —
in this case, I want the angles to disappear entirely
so that Cartesian outputs can be expressed directly
as functions of Cartesian inputs.
To take a simpler example,
I can’t figure out how to ask SymPy to eliminate $\theta$
from this system of two equations
so that the output $z_o$ is expressed directly as a function of $z$:

    solve([
        Eq(z, sin(𝜃)),
        Eq(zo, cos(𝜃)),
    ], zo)


If SymPy does have the capacity to eliminate intermediate variables,
then several of hours of work with the library —
and numerous visits to Stack Overflow —
left me without any insight into how to accomplish it.

## Third mistake: Thinking everything needed to be a SymPy symbol

The reason that I thrashed around trying to eliminate symbols was,
it turns out, because I had created too many!

I had expected that my angles $\theta$ and $\phi$
would be SymPy symbols in my Python code.
But as I tried to convince SymPy to eliminate them,
I stumbled on the approach
of treating `𝜃` and `𝜙` as plain Python names
for SymPy expression objects:

    𝜃 = asin(z)
    𝜙 = atan2(y, x)

The surprise came when I used these expressions to build a rotation matrix:

    rot_axis3(-𝜙)

Amazing!
Without my even asking,
SymPy has gone ahead and applied a series of trigonometric identities
to rewrite the matrix so that it can be computed directly
from my Cartesian inputs.

All that was needed
was to express the complete coordinate transformation in Python,
confident that SymPy would simplify the result:

    xo, yo, zo = rot_axis2(π/2-𝜃) * rot_axis3(-𝜙) * Matrix([xi, yi, zi])

This produces a formula for the first output coordinate:

    xo

And the second:

    yo

And the third:

    zo

I was done — I could now compute the rotated coordinates
without leaving the Cartesian domain!

## Icing #1: SymPy can print Python syntax

Next, I needed to substitute the formulae
back into my Python code.

With many mathematical libraries,
the procedure would have been tedious —
I would have had to manually type
each multiplication, addition, and ``sqrt()``
into Python without committing even a single one of my typical sign errors.

But, happily, a stray ``print()`` that I’d run
had revealed a delightful property of SymPy:
while it’s capable of producing beautiful fully rendered math
when used in a Jupyter notebook,
when asked to print plain text it produces fully valid Python
for the entire mathematically expression!

    print(xo)

I could paste the resulting expressions directly into Skyfield.

## Icing #2: SymPy supports sub-expression elimination

As you examined the output expressions, above,
you probably felt your redundancy hackles rising
as you noticed all of the repeated sub-expressions.
Pasting the three formulae into Python code
would result in a common value like ``sqrt(x**2 + y**2)``
getting recomputed a half-dozen times.

Happily, I ran across another SymPy routine named ``cse()``
which performs exactly the operation
I had been planning to do by hand —
it recognizes common sub-expressions and pulls them out:

    common, (xo, yo, zo) = cse([xo, yo, zo], numbered_symbols('t'))

    for symbol, expression in common:
        print(symbol, '=', expression)

    print()
    print('xo =', xo)
    print('yo =', yo)
    print('zo =', zo)

The result is Python code
that I can paste directly into Skyfield
without the temptation to perform any further tweaks —
letting me return to my star chart rendering
in the confidence that the underlying rotations have been computed flawlessly.
