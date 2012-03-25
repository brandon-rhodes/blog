<%inherit file="site.mako" />
<article>
  <div class="date">
    ${post.date.strftime('%Y %B %d').replace(' ', ' ')} —
    % for category in post.categories:
    <a href='${category.path}'>${category.name.title().replace(' ', ' ')}</a>
    % endfor
  </div>
  <h1>${post.title}</h1>
  ${post.content}
</article>
</div>

<%def name="title()">${post.title.split(':')[0]}: Brandon Rhodes</%def>
