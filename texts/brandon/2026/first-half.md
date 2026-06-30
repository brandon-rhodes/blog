---
date: 2026/06/29 17:41:00
permalink: http://rhodesmill.org/brandon/2026/first-half/
title: The first half of 2026
---

Even though I’m only able to work on my open source projects
as one hobby amongst others,
my projects saw several updates and releases
over the first half of 2026.
In case anyone is curious about what I’ve been up to,
here are the milestones that were reached over the past few months.

**January**

The first month of the year
saw a new release of my flagship astronomy library,
[Skyfield version 1.54](https://rhodesmill.org/skyfield/installation.html#v1-54-2026-january-18).

This new version is the product of a refactoring
that I had been working on since 2025.
Whenever you ask Skyfield to compute an `.apparent()` position,
it figures out how much the target’s light is deflected
by the Sun, Jupiter, and Saturn.
But what if a user wants to add additional deflectors to that list?
Or to remove one or two of them?
Or to turn deflection all the way off?

The list of deflectors used to be hard-coded in Skyfield’s internals.
This refactoring turned the deflection logic inside-out,
surfacing the list of deflectors
as an optional argument to `.apparent()`
that the caller can see and control.

The rewrite also accidentally fixed a bug in Skyfield
that I had never previously identified:
Skyfield was sometimes incorrectly computing the slight deflection
that Earth-based observers experience
from the Earth’s own gravitational field.
So an occasional 0.5 mas inaccuracy was eliminated
for observers on the Earth’s surface and in Earth orbit.

I also released a new version 2.24 of the Skyfield support library
[jplephem](https://pypi.org/project/jplephem/)
because NumPy has decided to stop supporting assignment
to an array’s `.shape` attribute,
and was starting to annoy users with deprecation warnings.

**February**

There are still folks out there
who use my [PyEphem](https://rhodesmill.org/pyephem/)
astronomy library,
whose `ephem` Python interface, while clunky, has provided the Python language
with access to an old C astronomy library
since PyEphem’s first release in 1998.

So when a user notified me that Python 3.14 had appeared,
I slogged into PyEphem’s CI files for GitHub Actions,
got the build working for the new Python version,
and made a release.

(But, alas,
don’t look for the release in the changelog on the PyEphem web site.
It turns out that the Sphinx documentation build for PyEphem is broken
because of breaking changes in Sphinx itself, setuptools, and jinja2.
I have no idea when I’ll have the time and inclination to fix it.)

**March**

For half a decade
I have been the custodian of the
[XEphem](https://xephem.github.io/XEphem/Site/xephem.html)
astronomy application for Unix and Mac,
after the retirement of its original author and maintainer,
Elwood Downey.

In January the XEphem community received the news
that Elwood’s long and productive life had reached its end,
which inspired me, over Feburary and early March,
to dig into XEphem’s open issues on GitHub
and make progress on some of the bugs and issues that folks had run into.
It also emboldened me —
I suppose because only now do I feel that I’m really captain of the ship —
to make a first big change of my own:
the arrow keys can now be used to scroll around
on the main Sky View showing the stars and planets.

If you’re curious about the recent updates,
click “Change log” in the left-hand menu
at the [project’s web site](https://xephem.github.io/XEphem/Site/xephem.html).

**April–June**

My main focus in the second quarter of the year
was wrangling a series of pull requests from a generous contributor,
Clément Robert,
that led to a new version 2.26
of the [sgp4](https://pypi.org/project/sgp4/) library,
which computes the positions of Earth satellites.
The library is used both by Skyfield
and by other Python projects that need satellite positions.
Thanks Clément’s work,
the module is now built atop the “Python Limited API”,
allowing a single binary wheel
to support multiple versions of Python.

Thanks to Clément’s code tweaks and metadata updates,
users will hopefully no longer need to open a new issue
every time a major Python version is released,
asking for sgp4 to be compiled and released.
Instead, the existing binary wheel will work seamlessly
with each new version of Python.

**Not at PyCon this year**

I didn’t attend PyCon 2026, in Long Beach, California, this year.

If any readers turn out to be seriously curious as to why,
then I’ll need to set aside some time to sit down
and engage in some introspection and writing.
But here are a few quick thoughts:

* My habit of annual week-long Grand Canyon hikes
  has been starting to expand into three and even, sometimes,
  four weeks of outdoor adventures each year,
  which leaves less time for conferences.

* I first attended PyCon, years ago, not just to listen,
  but in order to contribute my first conference talk.
  Every year since then,
  I’ve either been a speaker myself,
  or else I’ve been gathering ideas
  for upcoming talks at other conferences that have invited me.
  But it feels a bit like my era has passed —
  invitations to conferences no longer appear in my inbox,
  and even if I did get an invite today,
  I’m not sure I’d have anything new to say.
  I get all kinds of fun things done with Python each month,
  but using the same approach to programming
  that’s served me well for a couple of decades.

* Because of the collapse of my social media presence —
  I never did recover the kind of community
  that I enjoyed with other programmers
  when we were all on Twitter back in the late twenty-teens —
  I feel like I leave vibrant conversations at PyCon
  only to walk out into a world of silence.
  When I attended PyCon last year, in 2025,
  the conversations made my mind spark with ideas
  and new directions for my projects!
  But after a few weeks in the silence back at home,
  the sparks had gone out.

* It was easier to say “yes” to attending PyCon
  when it was either at a wonderful outdoor destination
  (Portland; Salt Lake City)
  or a city that was within driving distance
  (Cleveland; Pittsburgh).
  For whatever reason, Long Beach just didn’t feel like a can’t-miss
  conference destination for me.

As wider context,
I should mention that computer programming is not,
at the moment, my day job,
but one of my hobbies.

I paused my professional programming career a few years ago
when I purchased a historic home —
I assured my wife that it would only take me about a year to get it fixed up.
It turns out that I was, alas, underestimating the project!
I have now been working on it for much longer than a single year.
In case you want to follow along,
here’s the project on Instagram:

<https://www.instagram.com/goshens.harper.house/>

While I’m enjoying all of the new technical skills that I’m learning,
and I even attend a monthly meetup for folks who work on historic homes,
my emotions are conflicted:
doing work on a historic home doesn’t _scale._
My work only affects and improves this one single property.
Whereas, when I used to work full-time on software,
dozens or hundreds of people were able to benefit
from every tweak or improvement that I made.

Maybe I’ll find myself shifting myself back
to a majority-keyboard schedule within the next year or two?
We’ll see!

**What’s Next?**

With the sgp4 release now complete,
I feel like it’s time to take a deep breath and regroup.

Over the next month,
I want to read back through all open GitHub issues
for my various projects,
and make sure they all have up-to-date responses.
Sometimes I intend to reply at length about a complicated issue,
but don’t get around to it before needing to respond to a more pressing bug.

I might also finally abandon `setuptools` for my compiled projects.
A few experiments that I did last week
suggest that, for compiled Python modules like `sgp4` and `ephem`,
[meson-python](https://mesonbuild.com/meson-python/)
might result in a better workflow both locally on my laptop
and also in CI —
for example, by not writing build products
directly into the source tree.
Hopefully it doesn’t become an ordeal
that prevents me from making other progress on my projects!

Finally,
I think I’m going to tackle a small example Skyfield project:
a script that would compute a year’s worth of celestial events —
like New Moon and Full Moon, solstices, equinoxes, and conjunctions —
and write out an `.ics` iCalendar file
that the user can import into their favorite calendar program.
I’ll publish it as an example in the Skyfield docs.
It should be fun.
Over the years,
I have spent so much time maintaining my various projects
that I’ve often not had any time to actually _use_ them!
