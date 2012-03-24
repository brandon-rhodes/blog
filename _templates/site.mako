<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <title>${self.title()}</title>
  <link href="http://fonts.googleapis.com/css?family=Gentium+Book+Basic:700"
        rel="stylesheet" type="text/css">
  <link href="http://fonts.googleapis.com/css?family=Crimson+Text"
        rel="stylesheet" type="text/css">
  <link rel="stylesheet" type="text/css" href="/brandon/screen.css" />
  <!--[if IE]>
    <script src="http://html5shiv.googlecode.com/svn/trunk/html5.js"></script>
  <![endif]-->
</head>

<body>${next.body()}

<header class="header">
  <a class="site-title" href="/brandon/">
    <span class="title">Let's Discuss the Matter Further</span>
    <span class="author">Brandon Rhodes</span>
  </a>
  <span>
    <a href="http://feeds.feedburner.com/LetsDiscussTheMatterFurther"
       ><img title="Feed" src="/brandon/feed24.png"></a>
    <a href="http://twitter.com/#!/brandon_rhodes/"
       ><img title="Twitter" src="/brandon/twitter24.png"></a>
    <a href="http://brandon-rhodes.yelp.com/"
       ><img title="Yelp" src="/brandon/yelp24.png"></a>
    <a href="http://www.flickr.com/photos/brandonrhodes/"
       ><img title="Flickr" src="/brandon/flickr24.png"></a>
  </span>
</header>
</body>

<%def name="title()">${bf.config.blog.name}</%def>
</html>
