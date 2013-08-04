
Example PyCon talk proposals
============================

:Date: 2 August 2013
:Tags: Python

It was exactly one month ago that the PyCon site swung
back into action for another exciting year.
Talk submissions for
`Montréal 2014 <http://us.pycon.org/2014/>`_
are by now piling up quickly.

.. raw:: html

   <blockquote class="twitter-tweet"><p>You can now view the Call For Proposals announcement on our blog at <a href="http://t.co/kt7P2PinIY">http://t.co/kt7P2PinIY</a></p>&mdash; @pycon <a href="https://twitter.com/pycon/statuses/352174928126148610">July 2, 2013</a></blockquote>

This year, several people have asked me
what a real PyCon talk proposal actually looks like —
including a few students at the
`Hacker School <https://www.hackerschool.com/>`_ in New York,
where I served as a resident last month.
While the official PyCon
`Proposal Advice <http://us.pycon.org/2014/speaking/proposal_advice/>`_
page is excellent,
some people learn better by example.

So I am making public my PyCon talk proposals from several past years!

I include both 3 successes and 3 failures,
along with a few thoughts about each.
Remember that these only reflect how I myself tend to write proposals,
and that many factors vary from year to year —
including the interests and skill levels of selection committee members,
the number of talks competing in a given subject area,
and what fraction of talks can be accepted overall.

**“The Mighty Dictionary” (2010)** —
`Accepted proposal
<http://rhodesmill.org/brandon/2013/example-pycon-proposals/mighty-dictionary.txt>`__
— `Video and slides </brandon/talks/#mighty-dictionary>`__

    By the time I finish a proposal,
    I feel about halfway done writing the talk.
    That feeling is always hilariously inaccurate,
    but it hopefully signals the point at which
    I have gotten enough detail into the proposal
    for the committee to imagine what the talk will be like.

    I tend to outline each talk in 5-minute chunks,
    without worrying about anything more detailed.
    If each chunk can plausibly fill five minutes
    without taking more than five minutes to cover,
    then five chunks are enough to fill a 30-minute slot
    while leaving 5 minutes for questions at the end.

    I consider the Mighty Dictionary to be an especially strong proposal
    because, at each step, it describes a problem
    that then becomes the motivation for the material that follows.
    List lookup is too slow? Then we will index by hash!
    The dictionary will gradually fill? Then we will allocate more space!
    This pattern keeps listeners engaged,
    and helps them understand the emerging design.

.. more

**“Learning Hosting Best Practices From WebFaction” (2010)** —
`Accepted proposal
<http://rhodesmill.org/brandon/2013/example-pycon-proposals/webfaction.txt>`__
— `Video and slides </brandon/talks/#webfaction>`__

    I cannot imagine this talk being accepted today,
    in the age of containerized deployment solutions like Heroku.
    Also, the PyCon committee is more cautious every year
    about talks that mention a specific company or service.
    But in 2010, tips and techniques for deploying Python apps
    to a plain old shell account earned me a PyCon slot.

    I at least had the sense to suggest that each Webfaction feature
    was really a general technique,
    that could be taken and used elsewhere.
    And, wow, does anyone else remember
    `mod_wsgi <https://code.google.com/p/modwsgi/>`_?
    Crazy, crazy times.

**“Satchmo and GetPaid: sharing code between Django and Plone” (2010)** —
`Declined proposal
<http://rhodesmill.org/brandon/2013/example-pycon-proposals/satchmo-getpaid.txt>`_

    Ouch.
    Do you remember my disastrous Satchmo-and-GetPaid talk
    from PyCon 2010?
    No?
    Then please remember to thank the PyCon program committee!

    “I am now preparing to prototype some code.”
    The proposal rolls over and dies right there:
    this is pure talk-proposal Kryptonite.
    The committee knows immediately
    that the talk is not about something that I *have done*
    (note the perfect tense!),
    but about something that *I believe that I will learn*
    between now and PyCon.
    Whether the talk will have any content or not
    is entirely contingent upon code that has yet to be written.

    And, as the committee might have quietly been guessing,
    it turns out that the project never happened:
    the GetPaid code was simply not in a state
    that made me confident that I could move it forward,
    and a `disheartening sprint report
    <https://groups.google.com/forum/#!topic/getpaid-dev/AX-9wWXhmvs>`__
    helped convince me to put my energies
    elsewhere in the Python ecosystem.

**“Tree Rings in the Standard Library” (2011)** —
`Declined proposal
<http://rhodesmill.org/brandon/2013/example-pycon-proposals/tree-rings.txt>`__

    While I was able to contribute to PyCon 2011
    through my Sphinx tutorial and by moderating the WSGI panel,
    my one talk proposal was rejected.

    It is interesting to re-read this proposal now, three years later,
    because I can see several ideas
    that wound up being part of subsequent talks.
    I attempted a screed
    against the Standard Library’s object orientation,
    for example, in my PyOhio 2011 talk
    `“httplib, urllib2, and Their Discontents”
    <http://pyvideo.org/video/521/pyohio-2011-procedures-objects-reusability-q>`__
    while my interest in Python design patterns
    generated a `Design Patterns talk
    <http://pyvideo.org/video/1369/python-design-patterns-1>`__
    at PyOhio 2012.

    But my biggest surprise, upon re-reading,
    is how incurably vague the proposal is!
    No wonder it got rejected.
    The proposal is essentially a series of promises
    about the kind of examples that I am going to go find
    in the Standard Library once the talk is approved —
    without offering a single, actual, fleshed-out example.
    It promises content without actually enumerating that content,
    which is probably why it fails to follow my usual habit
    of actually outlining each 5-minute segment of the talk.
    It fails to outline the actual content
    for the simple reason that the content does not yet exist.

    My verdict?
    This is a research proposal, not a talk proposal.

..  2012
    Flexing SQLAlchemy's Relational Power
    Python, Linkers, and Virtual Memory

**“The Solar System in 5 Lines of Python” (2013)** —
`Declined proposal
<http://rhodesmill.org/brandon/2013/example-pycon-proposals/solar-system.txt>`__

    This proposal seemed solidly technical but was declined,
    while my speculative, theoretical, hand-wavy
    Naming-of-Ducks talk was accepted (see below).
    Neither proposal is detailed enough —
    neither includes any actual outline
    demonstrating that I was going to use 30 minutes effectively.

    Not only does the proposal fail to offer any source code
    showing what a 5-line orrery might look like,
    but it promises to cover many facts about the Solar System
    that are simply not Python-specific.
    And one usually combines the `IPython Notebook`_ and `matplotlib`_
    so that real-world, messy data
    can be loaded into a `Pandas`_ data frame
    and then sifted for real information.
    Planetary paths are, instead, sheer curves through empty space,
    and would not have highlighted any
    of the real strengths of Python’s scientific tools.

    Finally, we must remember that no proposal is made in a vacuum:
    several other scientific Python talks were on the table in 2013,
    most of them by scientists,
    who in many cases were the actual authors
    of the software in question.
    Fernando Perez, Travis Oliphant, and Titus Brown
    were among the names that wound up on the schedule.
    The committee had plenty of science-talk proposals to choose from.

**“The Naming of Ducks: Where Dynamic Types Meet Smart Conventions” (2013)** —
`Accepted proposal
<http://rhodesmill.org/brandon/2013/example-pycon-proposals/naming-of-ducks.txt>`__
— `Video and slides </brandon/talks/#naming-of-ducks>`__

    The program committee must simply have gotten a good vibe
    from this proposal,
    because it lacks any detailed outline
    on which they could have based their judgement.
    It is, instead, more of a sales pitch for ideas
    that had clearly not yet been reduced to actual talking points.

    Their wager paid off, but just barely!
    While the talk seems to have been a success —
    netting me an invitation to present it again
    at the `RuPy 2013 <http://13.rupy.eu/>`_ conference this autumn,
    among other positive reactions —
    the proposal’s ideas were almost too vague to work with,
    and I was finally able to write up some slides
    only a handful of days before the talk itself.

    Getting caught at the last minute without enough material
    is always a danger when I do not go ahead
    and write a detailed enough outline into the proposal itself!

----

So, there you have it!

I myself am surprised at how my quality
seems to have declined over the years —
nothing subsequent seems to quite equal the glorious detail
of my Mighty Dictionary talk proposal!
Re-reading it, in fact, has convinced me to be more concrete
in each of the proposals that I make this year.

I hope that these real-world examples
give those of you who are aspiring speakers some ideas
about formatting your own proposals,
as well as pointing out some errors to avoid.
Good luck!

.. include:: texts/links
