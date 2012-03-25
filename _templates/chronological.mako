<%inherit file="site.mako" />
<article class="chronological">
  <div class="date">Chronological Summary</div>
  % if True:
  <h1>All Posts Ever</h1>
  % else:
  <h1>Blog posts in the category:<br>${category}</h1>
  % endif
  % for post in posts:
  <p class="date2" rowspan="2">
    ${post.date.strftime('%Y %b %d').replace(' 0', ' ').replace(' ', ' ')}
  </p>
  <h2>
    <a href="${post.path}">${post.title}</a>
  </h2>
  <p class="excerpt">
    ${post.excerpt}…
  </p>
  % endfor
</article>
