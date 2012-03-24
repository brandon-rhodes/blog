<%inherit file="site.mako" />
<article>
  <div class="date">
    ${post.date.strftime('%Y %b %d').replace(' ', ' ')}
  </div>
  <h1>${post.title}</h1>
  ${post.content}
</article>
</div>

<%def name="title()">${post.title.split(':')[0]}: Brandon Rhodes</%def>
