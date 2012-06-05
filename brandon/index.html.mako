<%inherit file="site.mako" />
<%def name="title()">by Brandon Rhodes</%def>
<%def name="body_attributes()">class="index"</%def>
<%def name="css_links()"><link rel="stylesheet" type="text/css" href="/brandon/flickr.css" /></%def>

<article>
  <div class="date">About</div>
  <h1>Welcome</h1>

  <div class="image-reference">
    <a href="http://www.flickr.com/photos/brandonrhodes/4439207389/">
      <img src="http://farm5.staticflickr.com/4047/4439207389_44b4cd4d11_m.jpg">
    </a>
    <a href="http://www.flickr.com/photos/romanlily/5083723/">
      <img src="http://farm1.static.flickr.com/3/5083723_e31a17f2af_m.jpg">
    </a>
  </div>

  <p>
    I had worked for several years at a large institution
    when a friend invited me
    to <a href="http://pyatl.org/">Python Atlanta</a>,
    a local meetup for programmers.
    I had thought that books and blogs were keeping me up to date,
    but conversation with real people
    taught me so much more!
  </p>
  <p>
    I made the fateful decision
    to attend <a href="https://us.pycon.org/">PyCon 2008</a> and two
    <a href="http://plone.org/events/conferences">Plone conferences</a>,
    after which, I was hooked!
    A few months later I resigned my position
    and became an independent developer
    so that I could send myself
    to as many conferences as I wanted.
  </p>
  <p>
    My vocation has been transformed
    thanks to the Python community.
    While doing Python and occasional JavaScript programming
    for customers large and small,
    I focus on giving back to a movement that has given me so much.
    My talks and tutorials have taken me everywhere from the
    <a href="http://pyarkansas.wordpress.com/">middle of Arkansas</a>
    to the <a href="http://pl.pycon.org/">country of Poland</a>,
    <!-- (videos and slides are linked below), -->
    and people from several continents
    have offered improvements to the software
    that I myself contribute back to the community.
  </p>
  <p>
    I live in Bluffton, Ohio, with my wife Jackie and two cats.
  </p>
</article>

<article class="blog-summary">
  <div class="date">My Blog</div>
  <h1>Recent Posts</h1>
  <p>
    % for post in [ p for p in bf.config.blog.posts if not p.draft ][:5]:
    <span>${post.date.strftime('%Y %b %d').replace(' 0', ' ')} —</span>
    <a href="${post.path}">${post.title}</a><br>
    % endfor
  </p>
  <p>
    <a href="/brandon/all/">All Posts Ever</a>
  </p>
  <p>
    Tags:
    % for category, n in sorted((category, len(posts)) for (category, posts) in bf.config.blog.categorized_posts.items()):
    <a href="${bf.config.blog.path}/${bf.config.blog.category_dir}/${category.url_name}/"
       >${category} (${n})</a>
    % endfor
  </p>
</article>

<article>
  <div class="date">In print</div>
  <h1>My Book</h1>
  <a class="image-reference" href="http://www.amazon.com/gp/product/1430230037/ref=as_li_ss_il?ie=UTF8&amp;tag=letsdisthemat-20&amp;linkCode=as2&amp;camp=1789&amp;creative=390957&amp;creativeASIN=1430230037"><img border="0" src="http://ws.assoc-amazon.com/widgets/q?_encoding=UTF8&amp;Format=_SL160_&amp;ASIN=1430230037&amp;MarketPlace=US&amp;ID=AsinImage&amp;WS=1&amp;tag=letsdisthemat-20&amp;ServiceVersion=20070822" ></a>
  <p>
    I recently had the privilege of revising John Goerzen's
    <i>Foundations of Python Network Programming </i>to produce a
    <a href="http://www.amazon.com/gp/product/1430230037/ref=as_li_ss_il?ie=UTF8&amp;tag=letsdisthemat-20&amp;linkCode=as2&amp;camp=1789&amp;creative=390957&amp;creativeASIN=1430230037"
       >Second Edition</a>.
  </p>
  <p>
    I was stunned at how far Python has come.
    When the first edition was written in 2004,
    <tt>HTMLParser</tt> was the preferred screen scraper,
    <tt>xmlrpclib</tt> was the reigning protocol for async web requests,
    and the book skipped web frameworks entirely (it ignored Zope)
    to present chapters on <tt>cgi</tt>
    and <tt>mod_python</tt> instead!
  </p>
  <p>
    Take a look at the Second Edition if you are interested
    in a thorough tour of the network stack as seen from modern Python,
    including tutorial introductions to popular libraries like
    <tt>BeautifulSoup</tt>,
    <tt>lxml</tt>,
    and <tt>paramiko</tt>.
    All example programs from the book
    are available for free from
    <a href="https://bitbucket.org/brandon/foundations-of-python-network-programming"
       >my BitBucket repository</a>
    which also offers Python 3 versions of each script
    in case you have already made the leap!
  </p>
  <img src="http://www.assoc-amazon.com/e/ir?t=letsdisthemat-20&amp;l=as2&amp;o=1&amp;a=1430230037" width="1" height="1" border="0" alt="" style="border:none !important; margin:0px !important;" />
</article>

<article class="social-media">
  <div class="date">Social Media</div>
  <h1>Me, Elsewhere</h1>
  <div class="media">
    <div><a
      href="http://feeds.feedburner.com/LetsDiscussTheMatterFurther"
      ><img src="feed.png"></a>
    </div>
    <div><a
      href="http://twitter.com/#!/brandon_rhodes"
      ><img src="twitter.png"></a>
    </div>
    <div><a
      href="http://www.yelp.com/user_details?userid=1DOeEvKbUgflAcmDYRV_AQ"
      ><img src="yelp.png"></a>
    </div>
    <div><a
      href="http://www.flickr.com/photos/brandonrhodes/"
      ><img src="flickr.png"></a>
    </div>
    <div><a
      href="http://stackoverflow.com/users/85360/brandon-craig-rhodes"
      ><img src="stackoverflow.png"></a>
    </div>
    <br>
    <div><%include file="stackoverflow.html" /></div>
    <br>
    <div><%include file="twitter.html" /></div>
    <div><%include file="flickr.html" /></div>
  </div>
</article>
