---
categories: Python, Computing
date: 2012/04/13 07:05:36
permalink: http://rhodesmill.org/brandon/2012/logging_tree/
title: Introspect Python logging with logging_tree
---

It is frustrating that Python's ``logging`` module
cannot display the tangled tree of configured loggers
that often result from combining your own application code
with several libraries and frameworks.
So I have released a new Python package named
`logging_tree <http://pypi.python.org/pypi/logging_tree>`_,
which I announced last month during the
`PyCon 2012 <https://us.pycon.org/2012/>`_
`closing lightning talks <http://pyvideo.org/video/721/sunday-afternoon-lightning-talks-90-minutes>`_.
My package displays the current ``logging`` tree to help debugging,
and its output looks something like this::

    <--""
       Level WARNING
       Handler Stream <open file '<stderr>', mode 'w' at ...>
       |
       o<--[cherrypy]
           |
           o<--"cherrypy.access"
           |   Level INFO
           |   Handler Stream <open file '<stdout>', mode 'w' ...>
           |
           o<--"cherrypy.error"
               Level INFO
               Handler Stream <open file '<stderr>', mode 'w' ...>

The configuration shown by this tree, it turns out, causes a bug.
This diagram helped me fix a real-life application
for Atlanta startup `Rover Apps <http://roverapps.com/>`_,
who generously let me open-source ``logging_tree``
after I wrote the first version while helping them fix this bug.

In this post I am going to reproduce the problem
using a simple 10-line CherryPy application,
and then show how I used this ``logging_tree`` diagram
to craft a solution.
But, first, you need to know three things
about the Python ``logging`` module —
and I would like to thank Marius Gedminas for his
`recent post about logging levels <http://mg.pov.lt/blog/logging-levels>`_
that helped me correct something I had misunderstood.

.. more

* When you call a logger's ``log()`` method,
  or an equivalent helper like ``error()`` or ``debug()``,
  your message has only one opportunity to be discarded:
  it is compared against that logger's ``level`` attribute
  and thrown away if it is not at least that important.
  But if it passes this one test,
  then the message will be submitted not only
  to the logger's own handlers,
  but also to the handlers on all of the logger's parents —
  so a message accepted by logger ``'a.b.c'``
  will also be submitted to ``'a.b'``, ``'a'``,
  and the root logger ``''`` (whose name is the empty string).
  The ``level`` attribute of a parent logger *is completely ignored* —
  it applies only to messages submitted directly to that logger!

* Once a message passes this test against ``logger.level``
  and is accepted,
  the only thing that can stop it from being submitted
  to the handlers of every parent logger
  is for it to encounter a false ``propagate`` attribute along the way.
  After a message is submitted to a logger's handlers,
  the logger's ``propagate`` attribute is consulted
  to see whether the message should jump to the parent logger.
  The first false ``propagate`` encountered on the way up the tree
  kills the message, and no further propagation takes place.

* Confusingly, each handler can also choose
  to do its own individual filtering by a ``level``
  to decide which messages get output by that handler.
  Handlers can be configured with complex filters
  to determine which messages they are willing to output,
  and can even hand messages off to further handlers.

Some libraries also define custom filters and handlers.
While ``logging_tree`` will at least print their names,
it probably will not know anything else about them,
so you will have to read their source code
to learn more about how they work and behave.

The problem
-----------

We wanted to add some logging to our
`CherryPy <http://cherrypy.org/>`_ application,
so — as a simple first step — we grabbed the root logger ``''``
and tried writing a message::

    #!python
    import cherrypy
    import logging

    log = logging.getLogger('')

    class HelloWorld:
        def index(self):
            log.error('Test message')
            return 'Hello world!'
        index.exposed = True

    if __name__ == '__main__':
        cherrypy.quickstart(HelloWorld())

The result was disappointing.
The site displayed ``Hello`` ``world!`` in the browser
and produced a standard Apache log message,
but our own log message was nowhere to be seen.
I knew enough about ``logging`` to know that
a root handler was necessary if I wanted output,
so I tried adding one::

    #!python
    ...
    if __name__ == '__main__':
        log.addHandler(logging.StreamHandler())
        cherrypy.quickstart(HelloWorld())

The result was rather bizarre.
While our ``Test`` ``message`` appeared in the output,
the server now produced *two* copies of every CherryPy log message.

It was at this point that,
tired of trying to guess how the logging tree looked
by searching our entire code base
for calls to the ``logging`` package —
and searching the code of our third-party libraries, like CherryPy —
I instead wrote the first version of ``logging_tree()``
so that I could really see what was going on.
You can install it quite simply,
and it supports any version of Python from 2.3 through 3.2::

    #!bash
    pip install logging_tree

Invoking it from your application can be as simple as::

    #!python
    import logging_tree
    logging_tree.printout()

These two lines, added to my ``index()`` method,
printed the entire logger configuration to my terminal
the next time I reloaded the page.

Interpreting a tree
-------------------

This CherryPy application actually produces
a more complicated logging situation than in the simplified tree
used for illustration at the top of this post.
Here is what ``logging_tree`` really prints out —
in a few places I have used ellipses to keep lines
within the margins of my blog,
but this time no lines are omitted::

 <--""
    Level WARNING
    Handler Stream <open file '<stderr>', mode 'w' at ...>
    |
    o<--[cherrypy]
        |
        o<--"cherrypy.access"
        |   Level INFO
        |   Handler <cherrypy._cplogging.NullHandler object at 0x...>
        |   Handler Stream <open file '<stdout>', mode 'w' at ...>
        |   |
        |   o<--"cherrypy.access.166457196"
        |       Level INFO
        |       Handler <cherrypy._cplogging.NullHandler object at 0x...>
        |
        o<--"cherrypy.error"
            Level INFO
            Handler <cherrypy._cplogging.NullHandler object at 0x...>
            Handler Stream <open file '<stdout>', mode 'w' at ...>
            |
            o<--"cherrypy.error.166457196"
                Level INFO
                Handler <cherrypy._cplogging.NullHandler object at 0x...>

Loggers that have been created through actual calls to ``getLogger()``
are displayed with their names in double quotes.
When a logger only exists by implication,
but has never actually been named in a ``getLogger()`` call —
like the ``[cherrypy]`` node —
then its name is shown in square brackets.

Each logger displays its own ``Level`` that, as discussed above,
is only consulted when a message is submitted directly to that logger
using one of its methods like ``log()`` or ``error()``.

Propagation is turned on for all of these loggers,
as shown by the ``<--`` arrows that connect each logger to its parent.

You can see that this tree includes both built-in handlers
and also some custom ones defined in the CherryPy framework.
The ``logging_tree`` package tries to introspect the built-in handlers
to give you more information about them —
here, it displays the particular output files
to which the stream handlers will be printing —
but for the CherryPy loggers it has no choice
but to simply print their ``repr()``
and hope that you can make sense of them.

Solving the problem
-------------------

Thanks to this diagram, the problem is now clear:
because propagation is turned on,
CherryPy logging messages get printed by their own handlers
and *also* by the new handler we have installed at the root.
You can see this by imagining a new ``cherrypy.access`` error message
and following the propagation arrows that will take it from its
logger-of-origin up to the root, where our own handler is installed.

We can see, in fact, that CherryPy creates several loggers
to receive its Apache-style logging messages,
and goes ahead and suits those loggers up with handlers
that write the messages to the correct files.
Since I ran this application in debug mode from the command line,
these handlers are directed at ``<stdout>``
instead of actual log files.

The solution to my problem was to simply turn off propagation,
since CherryPy's handlers were already taking care of its messages::

    #!python
    logging.getLogger('cherrypy').propagate = False

The ``logging_tree`` package makes it very clear
when propagation has been turned off,
both by removing the ``<--`` arrow from next to the logger's name,
and also with a ``Propagate`` ``OFF`` message.
So this is how the tree looked following the fix::

    <--""
       Level WARNING
       Handler Stream <open file '<stderr>', mode 'w' at ...>
       |
       o   "cherrypy"
           Propagate OFF
           |
           ...

I hope that ``logging_tree`` proves useful
for many more Python programmers
as we all wrestle with logging misbehavior!
The package is available both
`on the Python Package Index <http://pypi.python.org/pypi/logging_tree>`_
and is also available as a
`project on GitHub <https://github.com/brandon-rhodes/logging_tree>`_
if you want to contribute.
