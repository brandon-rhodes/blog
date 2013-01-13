<%inherit file="site.mako" />
<article>
  <div class="date">
    ${post.date.strftime('%Y %B %d').replace(' 0', ' ').replace(' ', ' ')} —
    % for category in sorted(post.categories):
    <a href='${category.path}'>${category.name.title().replace(' ', ' ')}</a>
    % endfor
  </div>
  <h1>${post.title}</h1>
  ${post.content}
</article>
<article>
  <%include file="disqus.html" />
</article>

<%def name="title()">${post.title.split(':')[0]}: Brandon Rhodes</%def>
