---
categories: Computing, Python
date: 2011/05/04 23:00:28
permalink: http://rhodesmill.org/brandon/2011/wsgi-under-cherrypy/
tags: ''
title: Mounting WSGI Applications Under CherryPy
---

Today I got stuck between a rock and hard place —
or, more specifically, stuck between the assumptions
of Robert Brewer and those of Ian Bicking.
In case you ever try mounting a WSGI application
underneath a larger CherryPy application,
here is the story.

Simple WSGI grafting
====================

Robert Brewer's CherryPy_ is a Python web framework
of the controllers-and-methods variety.
CherryPy has a long, solid track record,
and is especially well-known
for shipping with a built-in production-quality web server.
The server is so good that it is sometimes used standalone,
without the actual CherryPy framework behind it,
to serve other Python web applications through their WSGI callable::

    #!python
    # Easy: putting a WSGI `app` behind the CherryPy HTTP server

    server = CherryPyWSGIServer(('0.0.0.0', 8001), app, numthreads=30)
    server.start()

Sometimes, however, it is nice to have the entire CherryPy
web framework running —
not merely its HTTP server —
in combination with an existing WSGI application.
This arrangement makes it easy to do things like
provide static resources
alongside more dynamic content generated in Python::

    #!python
    # More interesting: mounting `app` beneath a particular URL path
    # This works, but `app` gets no logging or error handling

    cherrypy.tree.graft(app, '/api')
    cherrypy.tree.mount(None, '/static', {'/' : {
        'tools.staticdir.dir': static_root,
        'tools.staticdir.on': True,
        }})
    cherrypy.engine.start()
    cherrypy.engine.block()

Although this arrangement works,
I soon received some unpleasant surprises.
When an exception was thrown inside of ``app``
the server never returned a response to the browser —
no ``500 Internal Server Error``,
no pretty traceback in development mode;
just a closed connection.
And neither errors nor successful requests inside of ``app``
resulted in access log messages;
CherryPy was completely silent about them.

This made it necessary for me to adjust my mental model
for how CherryPy operates.

I had always thought of the CherryPy framework
as having great big arms that wrapped around
my entire set of active controllers and applications,
so that it could catch exceptions and log HTTP requests
regardless of where in my tree they originated.
Now, however, I was forced to recognize
that the CherryPy ``try…except`` exception catcher
and its logging handlers
must only get involved
when invoking a controller inside of a real CherryPy app.
If an HTTP request is instead being handed off
to a WSGI application of my own devising,
then CherryPy took no further responsibility
for what happened —
I was on my own.

Finding WSGI components
=======================

Well, okay, I was not *really* on my own —
thanks to the wonderful Python community,
I sit surrounded by the rich and vibrant WSGI ecosystem
of well-supported interchangeable parts.
And logging and exception handling are standard features
that everyone needs, right?

Alas, the reality turned out to be far more murky.
After scouting about for some applicable WSGI
`middleware and utilities
<http://wsgi.org/wsgi/Middleware_and_Utilities>`_,
I started to sympathize with Python newbies
who complain about getting lost in the vast sea of broken software.
My long experience in the Python community
means that I often already know the “right tool” for the right situation,
which shields me from remembering what a mess Python newcomers face
when searching for even a simple solution.

For example, the popular ``flup`` package's documentation
promised that ``middleware.error`` contained an application
for catching WSGI application errors.

::

    $ pip install flup
    Downloading/unpacking flup...
    $ python -c 'import flup.middleware'
    Traceback (most recent call last):
      File "<string>", line 1, in <module>
    ImportError: No module named middleware

Drat, that must not be released yet.
What about this logging module listed on the WSGI wiki?

::

    $ pip install wsgilog
    Downloading/unpacking wsgilog...
    ImportError: No module named ez_setup

Wow, it does not even install.
Well, what about Werkzeug?

Armin Ronacher's `Werkzeug <http://werkzeug.pocoo.org/>`_
is renowned for its WSGI debugging middleware,
and it did actually install.
But when wrapped around my application,
it simply displayed a traceback of its *own* failure
to parse and display the error my application was encountering!

(If you want to know my guess as to the problem:
it appears that some of my Python code
is Unicode rather than plain ASCII.
To display it,
Werkzeug encodes it as UTF-8, prepends a BOM marker,
and passes it to the Standard Library's `compiler.parse()` function —
which then promptly explodes
because in Python 2.7 the AST represents a BOM using a new node type,
304, which other Standard Library code is not yet prepared to accept.
I have
`opened an issue <https://github.com/mitsuhiko/werkzeug/issues/51>`_
to see whether Armin thinks my guess makes sense
before I try reporting it in the Python bug tracker.)

And so I wound up using `Python Paste <http://pythonpaste.org/>`_
which installs and works quite cleanly,
and which let me add both basic logging
and error catching using just a few lines of code::

    #!python
    # Transform bare `app` into one that logs and 500s on exceptions

    from paste.exceptions.errormiddleware import ErrorMiddleware
    from paste.translogger import TransLogger

    app = ErrorMiddleware(app, debug=debug_flag)
    app = TransLogger(app, setup_console_handler=debug_flag)

    # Now we proceed as before to build our CherryPy application.

    cherrypy.tree.graft(app, '/api')
    ...

So far, so good.

The rock and the hard place
===========================

The Paste error handler let me diagnose and repair
my WSGI application in development mode.
When I started to switch things back over to production,
however, I received a surprise:
exceptions were always printed to ``sys.stderr``
even if I turned on every single option I could find,
in both CherryPy and Paste, for logging to actual files.

What was going on?

It turns out that I had run into a pair of hard-coded assumptions
that could not be solved by mere configuration.

In Ian Bicking's Paste project,
the traceback is directed to the ``wsgi.error`` file
provided in the WSGI environment::

    #!python
    # from paste/exceptions/errormiddleware.py

    class ErrorMiddleware(object):
        ...
        def exception_handler(self, exc_info, environ):
            ...
            return handle_exception(
                exc_info, environ['wsgi.errors'],
                ...)

The logic within ``handle_exception()`` unfortunately insists
on sending at least a little text
to the stream provided as its second argument,
even if you have turned on some of its other kinds of logging
(like sending an email or writing to a log).

And the identity of that ``wsgi.errors`` stream —
one of the few “live” objects inside of the WSGI environment,
whose dictionary values are mostly immutable objects like strings —
is hard-coded by Robert Brewer
inside of the module that invokes WSGI applications::

    #!python
    # from cherrypy/wsgiserver/__init__.py

    class WSGIGateway_10(WSGIGateway):

        def get_environ(self):
            """Return a new environ dict targeting the given wsgi.version"""
            ...
            env = {
                ...
                'wsgi.errors': sys.stderr,
                ...
                }
             ...
             return env

His definition of WSGI 1.0, then, sets ``wsgi.errors``
without (so far as I can see) any hope of amendment or recourse.
Thus the rock and the hard place:
Robert insisted that the default stream be ``stderr``,
and Ian's logging module insisted that something be written there.

Cutting the Gordian knot
========================

One of the great satisfactions of Python,
in the last analysis,
is that when you find yourself trapped in a situation like this
there are generally several ways to escape
and get back to more productive tasks,
like writing code of your own.

* An ugly possibility, always available as a last resort:
  I could simply monkey-patch,
  replacing one of the offending routines in Paste or CherryPy
  with a slightly different version of my own.

* I could update ``cherrypy.wsgiserver.wsgi_gateways``,
  a global dictionary mapping versions of the WSGI protocol
  to classes that implement them,
  so it offers my own subclass of ``WSGIGateway_10`` instead.

* I could globally replace ``sys.stderr`` when running as a daemon
  so that errant error messages get written to a file,
  and let Paste and CherryPy run without modification.

But each of the above ideas
has the disadvantage of making me adjust something big and global
to fix a problem which, in my program, is small and specific.

At the moment, therefore, I have
added my own tiny piece of WSGI middleware
between Robert's class and Ian's code
which overwrites ``wsgi.errors`` with something more appropriate::

    #!python
    # Adding three middlewares: error, logging, and my own

    app = ErrorMiddleware(app, debug=debug_flag)
    app = TransLogger(app, setup_console_handler=debug_flag)

    errlog = open('http-tracebacks.log', 'a', 0)

    def app2(environ, start_response):
        environ['wsgi.errors'] = errlog
        return app(environ, start_response)

    cherrypy.tree.graft(app2, '/api')

And my daemonized application is finally humming along
without the least desire to write to standard error!
To me, this is a great little example
of why a pluggable architecture like WSGI is so powerful
in a language like Python that makes it easy
to create and manipulate functions as first-class objects.

All of which leaves me with three thoughts.

First — looking at the install errors,
and how my attempt to use Werkzeug apparently revealed a bug
in Python's Standard Library itself —
I was painfully reminded of what a mess the Python ecosystem
must look like to those not familiar with its landscape.
If only we could communicate how rare experiences like this are,
once you develop a solid personal tool set
and learn your way around what works and what doesn't!

Second, I wish that CherryPy were willing to do logging
and exception handling for mounted WSGI applications.
I will have to ask Robert whether my approach here is even correct,
or whether there is some other way to call my own applications
without turning off so many features.

Finally, it occurs to me that instead of choosing Paste
and then spending far too long to make it work,
I should have tried out the competing middleware components
that Chris McDonough has produced as part of his
`Repoze project <http://repoze.org/repoze_components.html>`_.
I had not even thought of Repoze until writing this blog entry,
probably because of an unconscious assumption
that installing anything from the Zope world
would probably install a half-dozen dependencies.
But I just tried installing ``repoze.errorlog``
and it only requires a small package called ``meld3``
and, oddly enough, its competitor ``paste`` itself!
I should try it out before closing this issue.

Anyway, I hope this write-up helps someone else
who needs to use WSGI middleware
to backfill the features that are normally provided
as part of a large Python web framework.
And, of course, I look forward to comments from the community
about how my approach here could have been more elegant!

.. _CherryPy: http://www.cherrypy.org/
