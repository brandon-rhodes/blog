---
categories: Computing
date: 2011/05/13 10:09:46
permalink: http://rhodesmill.org/brandon/2011/adding-compass/
title: Adding Compass to your project
---

The `Compass CSS authoring framework <http://compass-style.org/>`_
has become one of the standard tools
that gets installed when I start working on a new web application.
I always version-control
not only the ``.scss`` Sass source files that I myself write,
but also the ``.css`` CSS files that Compass compiles from them.
That way, anyone who checks out the project
immediately gets a working web site
without having to install Compass —
or even having to know that it exists,
if they are not themselves involved in writing the CSS.

But those of us who work on the CSS do need Compass,
so I have a standard technique that I copy from project to project
that installs Compass into a small, local Ruby environment,
providing the same kind of isolation and reproducibility
that Python has taught me to know and love
thanks to `virtualenv <http://www.virtualenv.org/>`_.

The process goes like this.

First I create a ``compass/`` directory,
typically up at the top level of the project,
that initially contains nothing but a pair of shell scripts.
The first script, ``install.sh``, knows how to get Compass
downloaded and installed::

 #!bash
 #!/bin/bash
 # compass/install.sh - install Compass under the "./Gem" directory

 if ! which gem >/dev/null ;then
     echo 'Error: no "gem" command available'
     echo 'Please "sudo aptitude install rubygems1.8" or "ruby1.9.1"'
     exit 1
 fi
 BASE=$(dirname $(readlink -f $(which "$0")))
 cd $BASE  # the directory where this script lives
 gem install -i Gem compass
 gem install -i Gem compass-susy-plugin

When this shell script is run, a ``compass/Gem/`` directory
gets created with the ``compass`` command down inside of it.
To let me forget where the binary is located
and how it can be safely invoked,
a second shell script named ``compass.sh`` wraps up the details::

 #!bash
 #!/bin/bash
 # compass/compass.sh - properly invoke the "Compass" program

 BASE=$(dirname $(readlink -f $(which "$0")))
 export GEM_HOME=$BASE/Gem
 export RUBYLIB=$BASE/Gem/lib
 $BASE/Gem/bin/compass "$@"

I always tell my version-control system
to ignore the ``compass/Gem/`` directory
and the 5,115 files that Ruby creates beneath it;
instead, I simply remember to re-run ``install.sh``
after each fresh checkout
when I want to get to work on the CSS.

When I first start a project,
I need an initial set of ``.scss`` files to start editing,
which can be supplied through the Compass command ``create``.
Usually I want the CSS output to be written
somewhere outside of the ``compass/`` directory,
so my initialization steps go something like this::

 $ cd compass/
 $ ./install.sh
 $ ./compass.sh create
 $ rm -r stylesheets/    # where Compass wanted the output CSS!
 $ emacs config.rb
 # There, I adjust the line: css_dir = "../webapp/static/css"
 # Plus, I also tend to set: line_comments = false
 # Of course, use your editor-of-choice for this step!

I check into version control the ``config.rb`` file
and the ``compass/src/`` directory of pristine ``.scss`` files.
I tell my version-control system to ignore
the ``.sass-cache/`` directory that gets created inside of ``compass/``
each time the CSS is rebuilt.

Once those changes checked in,
I never need to run the ``create`` command again
for the whole lifetime of the project.
Instead, whenever I am ready to work on the CSS,
I simply open the ``.scss`` files in my editor
and in another window I do this::

 $ cd compass/
 $ ./compass.sh watch

Just as a good development web server
will auto-restart when you finish editing a file and hit *Save*,
the Compass ``watch`` command will sit patiently all day
and re-compile your Sass files to CSS whenever it sees you change them.
By leaving it running, I can edit a ``.scss`` file
and then hit *Reload* in my browser almost immediately to see the result
without having to stop and run any intermediate commands.

The files, therefore, that wind up in my version control are these::

 compass/compass.sh
 compass/config.rb
 compass/install.sh
 compass/src/_base.scss
 compass/src/_defaults.scss
 compass/src/ie.scss
 compass/src/print.scss
 compass/src/screen.scss

And, of course, I also version-control
the CSS files that Compass writes as output,
over where I put them in the “main directory” of my web application::

 webapp/static/css/ie.css
 webapp/static/css/print.css
 webapp/static/css/screen.css

This all works out extremely well.
Normal developers and deployers look under the ``webapp/`` directory
and see what looks like normal,
if preternaturally well-written and organized,
CSS files exactly where they expect to find them.
Only we CSS geeks on the project
know that they are written by shuffling over to the Compass directory
and firing up a program that compiles them from simpler source files.
And thanks to my handy little pair of shell scripts,
the Compass install itself is always completely automated.

Of course, as you can tell from the error message
that ``install.sh`` prints if it cannot find Ruby,
these scripts are aimed at an audience using Ubuntu or Debian.
Please note in your comments to this post
how you might expand those instructions
to help people using Fedora, MacOS X, or other operating systems!
