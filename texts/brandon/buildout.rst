
Buildout
========

.. class:: note

Update: these days, I tend to use a simple virtual environment
in conjunction with ``pip`` ``-e`` for development
instead of using buildout.
But buildout is still a simpler tool than most people realize,
and I like to think that this old screencast of mine
does a good job of illustrating a simplest-possible use case!

*January 2008*

This page is where I am collecting all of the hints
that I accumulate about using
`buildout <http://pypi.python.org/pypi/zc.buildout>`_,
the Python development and deployment technology
invented by the Zope folks.
To understand why I'm excited about it,
try watching my screencast of this talk that I gave at Python Atlanta:

.. raw:: html

   <div class="figure">
   <iframe width="420" height="315" src="//www.youtube.com/embed/HXvzzK9m2IA" frameborder="0" allowfullscreen></iframe>
   <p><a href="http://www.youtube.com/watch?v=HXvzzK9m2IA"
     >A Brief Introduction to Buildout</a> (YouTube)</p>
   </div>

**Q:** Where can I get a copy of the example module
that you used in your PyAtl talk?

**A:** You can download the source code for the ``lunar`` module
that I use as my central example in the talk right here:

http://rhodesmill.org/brandon/static/2008/lunar.tar.gz

**Q:** How can I start developing my Python package with buildout?

**A:** Move into the top-level directory of your package —
the directory that has your ``setup.py`` file inside —
and place two files there: ``bootstrap.py``,
which you can get in its most recent official version
`from this link <http://svn.zope.org/*checkout*/zc.buildout/trunk/bootstrap/bootstrap.py>`_,
and a ``buildout.cfg``
that describes the development tools you want available.
To gain the three tools I discuss in my presentations —
a Python interpreter,
access to the command-line scripts defined in your package,
and a way to invoke your test suite —
try out this sample ``buildout.cfg``::

    [config]
    mypkgs = lunar

    [buildout]
    develop = .
    parts = python scripts test

    [python]
    recipe = zc.recipe.egg
    interpreter = python
    eggs = {config:mypkgs}

    [scripts]
    recipe = zc.recipe.egg:scripts
    eggs = {config:mypkgs}

    [test]
    recipe = zc.recipe.testrunner
    eggs = {config:mypkgs}

Edit the first section of the file
(whose name is arbitrary, by the way;
``config`` just made it easy for me to remember why I put it there)
and change the package name ``lunar``
to the name you gave your package
in the ``name`` option of its ``setup.py``.
Then, run::

    $ python bootstrap.py
    $ ./bin/buildout

And you should find that a ``./bin/`` directory appears
with a ``python`` interpreter, a ``test`` runner,
and any command-line scripts your module
defines as ``console`` entry-points in its ``setup.py``.

**Q:** Does the buildout system destroy anything?

**A:** Yes;
buildout will consider itself the owner
of these three directories at the top level of your project,
so make sure that you are not using directories with these names
if you do not want them overwritten::

    develop-eggs/
    eggs/
    parts/

**Q:** What if I need a buildout that pulls eggs
from other locations than the main Python Package Index?

**A:** Add some URLs to your ``buildout.cfg`` —
they can point to any package index pages
that the ``easy_install`` command would normally be able to digest —
by adding this parameter (you can list several URLs if you want;
the following URL is simply for illustration)::

    find-links = http://download.zope.org/distribution/

**Q:** How can I avoid having every buildout on my system
download a separate copy of each egg it needs?

**A:** You should tell your buildouts to download eggs
into a single cache somewhere under your home directory.
The buildouts will still be safely isolated from each other,
since each version of an egg has its own filename!
But instead of modifying every single ``buildout.cfg`` file
to accomplish this, just create a ``~/.buildout/`` directory
inside of your home directory,
and place the following inside of a file named ``default.cfg``::

    [buildout]
    eggs-directory = /home/brandon/eggs

**Q:** How can I develop against another package's source code,
before it gets packaged up as an egg?

**A:** Download or checkout the other package's source code
into either a sub-directory of your project,
or another directory under your account.
Then, mention that directory's name in the ``develop`` declaration
in the main section of your buildout.
For example, in my presentation above I check out
the SQLAlchemy trunk into the directory ``sqlalchemy``,
and then adjust my ``develop`` line to look like::

    [buildout]
    develop = . sqlalchemy

But sometimes putting other projects
in a sub-directory of your own project can be annoying.
Your version control system might then start trying to include
the other project in your commits,
and if you have several projects
that need access to the development version of a particular library,
it might be annoying to have to check it out several times.
So I often check out several projects,
both my own and some others, into a single top-level directory,
and then have their ``develop`` lines look something like::

    [buildout]
    develop = . ../sqlalchemy ../gatech.identity

This way, a small cluster of applications and libraries
that I will be releasing as a set of eggs
can all get developed together.
But it does have the disadvantage
that if I actually check in my ``buildout.cfg``
while it looks this way,
then other developers will have to mimic
my directory structure (or re-edit the ``buildout.cfg``)
before they too can work on the project.

**Q:** Buildout keeps disrupting my development
by downloading newer versions of dependency packages when they appear,
which often have slight changes that break my application.

**A:** A quick fix is to add this line
to the ``buildout`` section of your ``buildout.cfg`` file::

    [buildout]
    newest = false

But I argue that this is inadequate protection,
because if you move to another machine and re-create the buildout,
then you are still vulnerable to getting
newer versions of dependencies
than the ones you were already working with.
And specifying ``newer`` ``=`` ``false`` provides no protection
for co-workers on other machines,
or for your customers who might later be installing
your product as an egg using ``easy_install``!

That's why the real solution is
to always specify absolute version numbers
in your project's ``setup.py``.
Instead of just requiring ``'pyephem'``,
require something specific like::

    install_requires=['pyephem==3.7.2.3'],

If you are afraid that you or your customers
might miss out on critical security updates to a package
by being stuck on a single version,
then leave the lowest version number unspecified by saying something like::

    install_requires=['sqlalchmey >= 0.4, < 0.5'],
