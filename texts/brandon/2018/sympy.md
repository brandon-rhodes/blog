
# Slowly learning SymPy while eliminating trigonometry from rotations


wanted to rotate without trig

THREE ERRORS

1. thought there was global state being created with each Eq
2. thought it would eliminate variables
3. wanted it to know all my variables

Icing: python expressions!
Icing: subexpression elimination!


My gradual elaboration of my Python astronomy library `Skyfield`_
has now reached the point of producing star charts.
Last weekend, I reached the hurdle
of rotating the vectors for the sky full of stars
so that some particular chosen point winds up at the chart's center.

The naive approach requires two dangerous crossings
of the boundary between the clean and confident realm of Cartesian coordinates
and the more troubled realm of spherical coordinates.
Given the position $(x, y, z)$ of the star one wants
at the center of the chart,
one first determines its spherical longitude and latitude —
the angle θ of the vector around the $xy$ plane
and its angle φ above the $xy$ plane:

$$ \eqalign{ \theta &= \tan^{-1}(y, x) \cr \phi &= \cos(z) } $$

With these angles one computes two matrices.
The first rotates any star $-θ$ around the $z$ axis
and the second rotates it up towards $+z$ by the angle $blah$.


Given an input star's position vector $x_i, y_i, z_i$,
the result of multiplication by these matrices
will be an output vector $x_o, y_o, z_o$
where the stars grouped around the target star in the sky
are now neatly grouped about the top of the $+z$ axis
and are ready for projection on to the flat surface of a chart.

    from sympy import *
    z, k = symbols('z k')
    solve(Eq(z, sin(k)), k)

Here be dragons

The approach outlined about is inelegant,
because it descends from the bright heights of Cartesian coordinates
into the dim sublunary world of spherical coordinates.

Cartesian coordinates spread importance and meaning
around the precision of the numbers with admirable uniformity.
Whatever the $x$ and $y$,
an adjustment $epsilon$ to $z$ moves the point of the vector
by the exact same amount —
whether the vector's length is a mere kilometer
or a parsec.

By contrast, the gravity the spherical coordinate
$θ$ for the angle around the $z$-axis
is deeply a function of whether the vector
points out along the equator of the sphere
or whether it is canted up or down towards one of the poles.

If the vector points out towards the equator,
adding one degree to $θ$ has the greatest possible effect:
the vector swings across one degree of sky.

But if the vector points up, nearly at the pole?
Then $θ$ makes hardly any difference at all
and its numeric investment in precision
is merely splitting hairs to decide where it points
along a tiny circumpolar line of latitude.

QUOTE about the problem

But I knew that there was a way out —
a way to avoid the expense and depressingness
of both the trigonometric functions and their inverses:
since the angles $θ$ and $blah$
are in this case derived from $x, y, z$ coordinates in the first place,
I knew that the proper substitutions and expansions
should generate formulae
for generating my output vector
solely in terms of the input vectors —
with the angles disappearing entirely!

To perform the math infallibly,
I turned to Python and its `SymPy` library
to perform the symbolic math.

My first mistake: thinking there was global state

While I know very well that well-written software
avoids maintaining global state,
SymPy looked enough like older systems I had experience with —
like Mathematica —
that I repeatedly thought of myself
as feeding knowledge into SymPy's central data store
with which it could render a result.

But that's simply not how SymPy works.
When you say something like:

Eq(z, sin(blah))

— you are not enrolling this fact in a magical SymPy data store
that is going to remember it later
when you then ask it to solve for something:

solve(Eq(y, 3))

The ``solve()`` routine is in fact a true function:
it knows only the information you provide as its arguments.

It also did not help that —
as I labored under the delusion
that I was slowly feeding new facts into SymPy —
that I also kept writing ``a = b`` when I should have written ``Eq(a, b)``.
This despite the prominent warning in the SymPy documentation,
which I suppose I should have read more thoroughly
instead of simply jumping to the part I thought I needed:

QUOTE

It repeatedly confused me that I would write:

create two symbols
accidentally overwrite one

And then try to:

do something

And see that result.
It took several tries before I realized that ``=``
is everywhere and always in Python the assignment operator —
in this case discarding the previous ``Symbol`` object
to which the name xx referred
and now using the name xx to refer to the new expression object
I had just created.

My second mistake: I though SymPy could eliminate variables

I love thinking about trigonometry in the "forwards" direction:

z = sin(blah)

— because it always feels backwards
for it to be my job to flip the equation around
to an arc-trigonometric function:

blah = asin(z)

So I wanted it to do:

solve([
    Eq(z, sin(blah)),
    Eq(z, cos(blah)),
    Eq(xo, xi * sin(blah) + yi * cos(blah)),
], [xo])

— and somehow convince SymPy to do the work
of eliminating blah from the system of equations
and formulating xo purely in terms of xi and yi.

If SymPy has that capability,
then several of hours of work with the library —
and numerous visits to Stack Overflow —
have left me without any insight into how to accomplish it
automatically.

I did see that I could substitute:

solve(Eq(z, sin(blah)), blah)
solve(Eq(z, cos(blah)), blah)
substitute???
Eq(xo, xi * sin(blah) + yi * cos(blah)), [xo])

But I abandoned the attempt to move forward with substitution.
The resulting code was more work to write,
and more verbose to read,
than simply inverting the trigonometric functions in my own head.

My third mistake: Thinking everything needed to be a SymPy symbol

The entire reason I thrashed about trying to eliminate symbols was,
it turns out, because I had created too many!

Instead of defining a symbol for the intermediate angle quantities,
and then complaining that SymPy had no easy way to get rid of them,
I stumbled upon the idea
of treating `θ` and `blah` as plain Python names
for SymPy expressions.
Let's first step:


Then I did this:

The surprise came when I printed the result:

Substation had happened!
Because I had never formally told SymPy that θ existed,
but simply used it myself as my own personal Python name
for a larger expression,
SymPy launched into exactly the substation and simplification
that I wanted.

Icing: python expressions!

Once the operation was complete,
I needed to substitute the resulting formula
back into my Python code.

With many mathematical libraries,
the result would have been tedious —
manually typing the dozens of multiplications, additions,
and ``sqrt()`` calls demanded by the math,
all while trying not to commit one of my typical sign errors.

But, happily, a stray ``print()`` that I had run while confused
about a particular subexpression
had revealed to me a delightful property of SymPy:
that while it's capable of producing beautiful fully rendered math
when used in a Jupyter notebook,
its native language when asked to print plain text
is to produce fully valid Python
for the entire mathematically expression:

show

This meant that, my rotation and projection complete,
I could paste the resulting expressions
directly in Skyfield —
saving tedious work and avoiding several kinds of possible error.

Icing: subexpression elimination!

As you can see,
the expression above contains several repeated sub-expressions.
While expressions like the one above
performed just fine when I pasted them into Skyfield,
it was a slight conceptual annoyance
that a quantity like ``...``
was being redundantly computed several times
in the course of evaluation.

I planned at some point to dive in
and manually factor out the common sub-expressions,
but deferred the work
until my sky chart was complete
and I knew that I wouldn't be doing further iteration
on the rotations.

It was by accident that I ran across another SymPy routine,
``cse()`` —
which performs exactly the operation
I had been planning to do by hand!
To wit:

cse(...)

And the result is Python code
that I can paste directly into Skyfield
without even the temptation to perform final tweaks —
and that, as the happy result
after several long hours of misunderstanding SymPy,
will let me rotate all the vectors I want
without a single trigonometric function anywhere in sight!
