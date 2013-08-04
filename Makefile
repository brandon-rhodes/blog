# Establish the default target when "make" is run without arguments.

all:
.PHONY: all

# Create a "cache" directory to hold intermediate results.

ignored := $(shell mkdir -p cache)

# Custom "find" that returns filenames without the directory name
# prepended, so that we can "addprefix" instead of "patsubst" them.

find = $(shell find $(1) -printf '%P\n')

# Compile posts into an intermediate form in the cache directory, so
# that pages and feeds can share the work done during parsing.

post_names := $(call find, texts/brandon -wholename '*/2*.rst')
post_caches := $(addprefix cache/, $(post_names))

all: $(post_caches)
$(post_caches): cache/%: texts/brandon/% bin/cache-post
	bin/cache-post $< $@

# Learn which tags were used in which posts.

cache/tags: $(post_caches) bin/cache-tags
	bin/cache-tags $(post_caches) cache/tags

include cache/tags

#

statics := $(addprefix output/, $(call find, static -type f))

input_html := $(call find, texts -name '*.html')
index_html := $(addprefix output/, $(filter %/index.html, $(input_html)))
other_html := $(patsubst %.html, output/%/index.html, \
                $(filter-out $(index_html), $(input_html)))

input_rst := $(call find, texts -name '*.rst')
index_rst := $(addprefix output/, $(filter %/index.rst, $(input_rst)))
other_rst := $(patsubst %.rst, output/%/index.html, \
               $(filter-out $(index_rst), $(input_rst)))

outputs := $(statics) $(index_html) $(other_html) $(index_rst) $(other_rst)

directories := $(sort $(dir $(outputs)))
ignored := $(shell mkdir -p $(directories))

style := templates/layout.html bin/format bin/helpers.py

all: $(outputs)

$(statics): output/%: static/%
	cp $< $@

$(index_html): output/%: texts/% $(style)
	bin/format $< $@

$(other_html): output/%/index.html: texts/%.html $(style)
	bin/format $< $@

$(index_rst): output/%.html: texts/%.rst $(style)
	bin/format $< $@

$(other_rst): output/%/index.html: texts/%.rst $(style)
	bin/format $< $@
