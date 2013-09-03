# Establish the default target when "make" is run without arguments.

all:
.PHONY: all

# Create a "cache" directory to hold intermediate results.

ignored := $(shell mkdir -p cache)

# Custom "find" that returns filenames without the directory name
# prepended, so that we can "addprefix" instead of "patsubst" them.

find = $(shell find $(1) -printf '%P\n')

# Compile source texts into an intermediate data structure in the
# "cache" directory, so that parsing only needs to occur once, and both
# pages and feeds can incorporate the resulting HTML.

rst_inputs := $(call find, texts -name '*.rst')
rst_caches := $(patsubst %.rst, cache/%.dict, $(rst_inputs))

all: $(rst_caches)
$(rst_caches): cache/%.dict: texts/%.rst bin/cache-text
	bin/cache-text $< $@

ipynb_inputs := $(call find, texts -name '*.ipynb')
ipynb_caches := $(patsubst %.ipynb, cache/%.dict, $(ipynb_inputs))

all: $(ipynb_caches)
$(ipynb_caches): cache/%.dict: texts/%.ipynb bin/cache-text
	bin/cache-text $< $@

# Learn which tags were used in which texts.

cache/tags: $(rst_caches) bin/cache-tags
	bin/cache-tags $(rst_caches) cache/tags

include cache/tags

# Build pages.

cache_all := $(call find, cache -name '*.dict')
cache_indexes = $(filter %/index.dict, $(cache_all))
cache_others = $(filter-out %/index.dict, $(cache_all))
html_indexes = $(patsubst %.dict, output/%.html, $(cache_indexes))
html_others = $(patsubst %.dict, output/%/index.html, $(cache_others))

all: $(html_indexes) $(html_others)

$(html_indexes): output/%.html: cache/%.dict bin/format
	bin/format $< $@

$(html_others): output/%/index.html: cache/%.dict bin/format
	bin/format $< $@

# Build feeds.

rss := $(patsubst %, output/brandon/category/%/feed/index.xml, $(tags))
all: $(rss)
$(rss): output/brandon/category/%/feed/index.xml: bin/build-feed cache/tags
	bin/build-feed cache/tags $* $@

# Static files are simply copied into the output directory.

statics := $(addprefix output/, $(call find, static -type f))
all: $(statics)
$(statics): output/%: static/%
	cp $< $@

notebooks := $(addprefix output/, $(call find, texts -name '*.ipynb'))
all: $(notebooks)
$(notebooks): output/%: texts/%
	cp $< $@

# Pre-create output directories.

directories := $(sort $(dir $(html_indexes) $(html_others) $(statics)))
ignored := $(shell mkdir -p $(directories))
