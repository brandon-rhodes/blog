---
categories: Python, Computing
date: 2012/06/04 23:58:03
permalink: http://rhodesmill.org/brandon/2012/screen-scraping-chapter-updates/
title: Updates to my free chapter on Screen Scraping
---

.. raw:: html

   <a class="image-reference" href="http://www.amazon.com/gp/product/1430230037/ref=as_li_ss_il?ie=UTF8&tag=letsdisthemat-20&linkCode=as2&camp=1789&creative=390957&creativeASIN=1430230037"><img border="0" src="http://ws.assoc-amazon.com/widgets/q?_encoding=UTF8&Format=_SL160_&ASIN=1430230037&MarketPlace=US&ID=AsinImage&WS=1&tag=letsdisthemat-20&ServiceVersion=20070822" ></a>

There are two updates that I need to share with readers
of the “Screen Scraping” chapter of
`Foundations of Python Network Programming <http://www.amazon.com/gp/product/1430230037/ref=as_li_ss_il?ie=UTF8&tag=letsdisthemat-20&linkCode=as2&camp=1789&creative=390957&creativeASIN=1430230037>`_,
the book I revised for Apress in 2010 —
a rewrite of the original edition by John Goerzen
that was published in 2004.
The chapter is now available for free,
right here on my web site:

.. admonition:: Free chapter!

   `“Screen Scraping with BeautifulSoup and lxml” <http://rhodesmill.org/brandon/chapters/screen-scraping/>`_

I chose the screen-scraping chapter for release
because the topic is so practical.
During the most recent PyCon, the book's fans all sounded surprised
as they told me how useful the book was —
apparently “Network Programming” in the title
made them think that the book
would only cover primitive byte and packet operations,
instead of tackling popular application-level topics
like JSON, SSH, message queues, and server architecture.

Even though barely a year and a half
has passed since the book's release,
there are already two ways that the chapter's advice has become dated —
we should be proud that the Python ecosystem moves so quickly!
So I have inserted two “From the Future” warnings into the text
as it appears here on my web site.
The reasons are:

* In 2011, Kenneth Reitz earned lasting fame by releasing the
  `requests <http://docs.python-requests.org/en/latest/index.html>`_
  library, which offers a beautiful new Pythonic API
  for programs that want to act as an HTTP client.
  His package has eclipsed all of the other options
  that the chapter originally mentioned — ``urllib2``, ``httplib``,
  and even ``mechanize`` — to become the library of choice
  for Python programmers
  who need to fetch information from a web site.

* More recently, the
  `BeautifulSoup <http://www.crummy.com/software/BeautifulSoup/>`_
  project has revived and released a brand new
  `beautifulsoup4 <http://pypi.python.org/pypi/beautifulsoup4>`_
  library on the Python Package Index
  that not only fixes the fragile parser problems
  that were plaguing the project's 3.2 release back in 2010,
  but is fully compatible with both Python 2 and Python 3
  for those who are making the move to the newer version
  of the Python language.

With those qualifications,
the chapter's information should still be accurate;
but let me know here in the comments
if you can think of other updates that might benefit readers.

