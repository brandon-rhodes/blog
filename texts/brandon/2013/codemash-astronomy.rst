---
categories: Computing, Emacs, Python, PyEphem
date: 2013/01/12 23:58:04
permalink: http://rhodesmill.org/brandon/2013/codemash-astronomy/
title: IPython Notebook and Astronomy at CodeMash
---

Another CodeMash is over!
Bacon has been eaten,
the Kalahari water park has echoed
with talks about languages both static and dynamic,
and one of the world's most eclectic programming conferences
has sent more than a thousand attendees away happy.

.. raw:: html

   <blockquote class="twitter-tweet"><p>You're missing @<a href="https://twitter.com/brandon_rhodes">brandon_rhodes</a> <a href="https://twitter.com/search/%23codemash">#codemash</a> talk. <a href="http://t.co/4Y4KQ8Ax" title="http://twitter.com/benjaminws/status/289772156034891778/photo/1">twitter.com/benjaminws/sta…</a></p>&mdash; Benjamin W. Smith (@benjaminws) <a href="https://twitter.com/benjaminws/status/289772156034891778" data-datetime="2013-01-11T16:34:01+00:00">January 11, 2013</a></blockquote>
   <script async src="//platform.twitter.com/widgets.js" charset="utf-8"></script>

I was quiet when attending my first CodeMash in 2012,
but for 2013 I proposed a talk of my own that,
to my great delight, was accepted!
It was not recorded, but here are the slides and source code:

→ Slide deck “`Touring the Universe with Scientific Python
<http://rhodesmill.org/brandon/slides/2013-01-codemash/slides.html>`_”

→ GitHub repository “`astronomy-notebooks
<https://github.com/brandon-rhodes/astronomy-notebooks>`_”

.. raw:: html

   <!--more-->

It was great fun to tout a genuine Python superpower
in front of an attentive crowd yesterday,
and to explain my excitement about how
`IPython Notebook
<http://ipython.org/ipython-doc/dev/interactive/htmlnotebook.html>`_
and the scientific libraries behind it
can impact education, research, and collaboration.

.. raw:: html

   <blockquote class="twitter-tweet"><p>Absolutely awesome talk from @<a href="https://twitter.com/brandon_rhodes">brandon_rhodes</a> on Scientific Python. Best of <a href="https://twitter.com/search/%23codemash">#codemash</a> thus far.</p>&mdash; Mike Busch (@mikelikesbikes) <a href="https://twitter.com/mikelikesbikes/status/289778060486651904" data-datetime="2013-01-11T16:57:28+00:00">January 11, 2013</a></blockquote>

I chose astronomy as my science topic because of its familiarity —
every sighted person has seen the stars, I reasoned,
and everyone seems to remember from school
that the planets revolve around the sun —
so I could jump right in to the visualizations
without having to explain what an “orbit” is.
Over the course of my talk I switched between my slides
and a browser running a live IPython Notebook server
with a series of notebooks (available at the GitHub link above)
that illustrate 2D plotting, 3D visualization, and numeric processing.

I submitted the talk proposal back in September
as the Python community was first mourning
`John Hunter <http://numfocus.org/johnhunter/>`_.
I thought it would be fitting if this were the year
that CodeMash featured John's work,
and IPython Notebook had caught my attention at PyCon 2012.
But what *really* gave my talk its momentum
was seeing `Fernando Perez <http://fperez.org/>`_
bring down the house
with his concluding keynote at `PyCon Canada <http://2012.pycon.ca/>`_
in November —
I have never seen a live demo generate
such sustained eruptions of applause!
In fact, the “IPython Examples” notebook with which I closed my talk
is essentially a list of IPython features
that I did not even know existed until I saw Fernando speak.

Here is Fernando's talk from November:

.. raw:: html

   <iframe width="420" height="315" src="http://www.youtube.com/embed/F4rFuIb1Ie4" frameborder="0" allowfullscreen></iframe>

Now that my CodeMash talk is over,
I will be turning my attention back to the astronomy notebooks.
Their code is so much longer and more awkward than I would have liked!
This is the first time that I have made heavy use
of my astronomy APIs in conjunction with NumPy and SciPy,
and the results are not pretty.
Watch for notable improvement in the coming months
as I practice “Notebook-driven” development
and begin making things simpler!

