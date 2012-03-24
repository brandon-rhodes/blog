######################################################################
# This is your site's Blogofile configuration file.
# www.Blogofile.com
#
# This file doesn't list every possible setting, it relies on defaults
# set in the core blogofile _config.py. To see where the default
# configuration is on your system run 'blogofile info'
#
######################################################################

######################################################################
# Basic Settings
#  (almost all sites will want to configure these settings)
######################################################################
## site_url -- Your site's full URL
# Your "site" is the same thing as your _site directory.
#  If you're hosting a blogofile powered site as a subdirectory of a larger
#  non-blogofile site, then you would set the site_url to the full URL
#  including that subdirectory: "http://www.yoursite.com/path/to/blogofile-dir"
site.url = "http://rhodesmill.org"

#### Blog Settings ####
blog = plugins.blog

## blog_enabled -- Should the blog be enabled?
#  (You don't _have_ to use blogofile to build blogs)
blog.enabled = True

## blog_path -- Blog path.
#  This is the path of the blog relative to the site_url.
#  If your site_url is "http://www.yoursite.com/~ryan"
#  and you set blog_path to "/blog" your full blog URL would be
#  "http://www.yoursite.com/~ryan/blog"
#  Leave blank "" to set to the root of site_url
blog.path = "/brandon"

## blog_name -- Your Blog's name.
# This is used repeatedly in default blog templates
blog.name = "Let’s Discuss the Matter Further"

## blog_description -- A short one line description of the blog
# used in the RSS/Atom feeds.
blog.description = "Thoughts and ideas from Brandon Rhodes"

## blog_timezone -- the timezone that you normally write your blog posts from
blog.timezone = "US/Eastern"

## Markdown extensions
## These are turned off by default, but turned on
## to show examples in /blog/2009/07/24/post-2/
filters.markdown.extensions.def_list.enabled = True
filters.markdown.extensions.abbr.enabled = True
filters.markdown.extensions.footnotes.enabled = True
filters.markdown.extensions.fenced_code.enabled = True
filters.markdown.extensions.headerid.enabled = True
filters.markdown.extensions.tables.enabled = True

# And more:

blog.custom_index = True
blog.disqus.enabled = True
blog.disqus.name = 'rhodesmill'
blog.posts_per_page = 9999
blog.post.default_filters['rst'] = 'rst, rst_syntax_highlight'
blog.post_excerpts.enabled = True
blog.post_excerpts.word_length = 50

# Disable the creation of archives.  We need no archives.

def patch_everything():
    """A function scope, to avoid polluting the _config namespace."""

    def do_nothing(*args, **kw):
        pass

    from mock import patch as patch
    import shutil

    import blog.archives
    import blog.categories
    import blog.chronological

    blog.archives.write_monthly_archives = do_nothing
    blog.archives.write_index = do_nothing

    write_blog_chron = blog.chronological.write_blog_chron

    def wrapped_write_blog_chron(*args, **kw):
        write_blog_chron(*args, **kw)
        shutil.move('_site/brandon/page/1', '_site/brandon/all')

    blog.chronological.write_blog_chron = wrapped_write_blog_chron

    # Eliminate "page 1" of each category in favor of only having each
    # category's main index.html.

    d = patch('shutil.copyfile', shutil.move)
    blog.categories.write_categories = d(blog.categories.write_categories)

patch_everything()
