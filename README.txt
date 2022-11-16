
Each text inside of the `texts/` directory is read and turned into a
Python dictionary, whose repr is written to a corresponding file in the
`cache/` directory.  Dictionary keys needed by further processing steps
are:

'path' - relative path, like: 'cache/brandon/2013/example-pycon-proposals.dict'
'body' - HTML
'title' - Unicode title
'tags' - set of textual tags for the article, like {'python', 'science'}
'datetime' - the date and time of publication as a `datetime`
'info'?  (see format)

Optional fields are:

'add_disqus' - whether to include Disqus comments at the page bottom (DISABLED)
'add_mathjax' - whether the HTML needs post-processing with MathJax
