---
categories: Computing
date: 2012/05/07 22:01:40
permalink: http://rhodesmill.org/brandon/2012/home-directory-vc/
title: Moving home directory version control out of your way
---

If you keep your home directory under version control,
then you may know the sinking feeling
that comes from sitting down at work after a late night,
looking for that brilliant fix you made right before bed,
and finding that your commit is nowhere to be found.
What happened?

Upon arriving home,
you discover that your final conscious act the previous night
was an accidental commit of your home directory —
you committed, say, a tiny experimental change to your ``~/.profile``
from last week
when you really meant to be committing a patch to ``~/big/project``
to resolve the latest show-stopping bug.
You were too tired to notice
that the version control system listed the wrong files
as you typed the commit message into your editor.

This can, of course, happen if you run ``git`` or ``hg``
while you are sitting in the wrong directory.
But, more subtly, this can happen
if you are sitting in the *correct* directory
but call the wrong *command*.
If ``~/big/project`` was, for example,
checked out using Mercurial or Subversion,
then a ``git`` ``commit`` in that directory
will patiently search up the directory tree,
find your ``~/.git`` directory,
and look for changed dotfiles or commands to commit instead.

For those of us with several version control systems going at once,
in fact, it is a bad idea to have *any* two projects be “concentric” —
where a directory under the control of one version control system
wraps another project under different control.
I really prefer for each directory in the file system
to have exactly one version-control directory
in its tree of ancestors.

So how can you safely version control your dotfiles?
The solution is to keep your ``~/.git`` or ``~/.hg`` directory
out of the way during normal operation —
for example, by appending ``.off`` to its name —
then moving it back into place
when you explicitly want to perform a version control operation
on your dotfiles.
One approach would be to create a shell script like this::

    #!bash
    # ~/bin/homedir-git
    # Like git, but turns your homedir "on" first

    mv ~/.git.off ~/.git
    git "$@"
    mv ~/.git ~/.git.off

However, I found this approach unwieldy.
For one thing, the name of the command was always difficult to type
because I am so strongly conditioned to type the plain, unadorned
version control command instead.
Another problem is that my shell's command-line completion
suddenly did not know to offer the usual version-control subcommands
because ``homedir-git`` or ``homedir-hg``
is not a command it recognized.

So my actual solution has been to create a command
to *toggle* home directory version control on and off.
That way, I can turn it on;
let my normal muscle memory take over
as I craft and execute version-control operations;
and then turn it off again::

    #!bash
    # ~/bin/home-toggle

    if [ -d .git.off ] ;then
        mv ~/.git.off ~/.git || exit 1
        echo Home directory version control activated
    else
        mv ~/.git ~/.git.off || exit 1
        echo Home directory version control deactivated
    fi

Actually, I named my own copy of this shell script ``,home``
because — as you might remember — I
`name my shell scripts starting with a comma <http://rhodesmill.org/brandon/2009/commands-with-comma/>`_.
But you get the idea.
And, of course, I check this shell script into version control
along with the rest of the suite of customizations
that I need on every system where I type.

This whole idea is trivial, obvious,
and so simply implemented as to be hardly worth mentioning.
But those of us who have been using a Unix environment for decades
know that these kinds of tiny micro-customizations
for making our lives easier,
while they are each so simple,
accumulate together into a really amazing result:
an environment that offers very little friction
because, each time your dotfiles are checked out
to your account on a new machine,
it instantly becomes an environment
where every annoyance —
every stone that has ever made you stumble —
has already been accounted for and worked around.

The lack of friction at a well-customized command line
can be really astounding if you have been putting up
with the defaults your entire life.
I hope that this simple example
encourages you to stop in your tracks
the next time something gets in your way for the third,
fourth, or hundredth time, and that you will ask:
“Could I solve this with a simple shell script?”
