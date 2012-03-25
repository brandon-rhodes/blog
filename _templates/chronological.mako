<%inherit file="site.mako" />
<article class="chronological">
  % if 'category' not in context.keys():
  <div class="date">Chronological Summary</div>
  <h1>All Posts Ever</h1>
  % else:
  <div class="date">Category Summary</div>
  <h1>Posts tagged “${str(context['category']).title()}”</h1>
  % endif
  % for post in posts:
  <p class="date2" rowspan="2">
    ${post.date.strftime('%Y %b %d').replace(' 0', ' ')}
  </p>
  <h2>
    <a href="${post.path}">${post.title}</a>
  </h2>
  <p class="excerpt">
    ${post.excerpt}…
  </p>
  % endfor
</article>
