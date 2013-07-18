
find = $(shell find $(1) -printf '%P\n')

statics := $(addprefix output/, $(call find, static -type f))
indexes := $(addprefix output/, $(call find, texts -name index.html))
pages := $(patsubst %.html, output/%/index.html, \
           $(call find, texts -name '*.html' ! -name index.html))

directories := $(sort $(dir $(statics) $(texts_out)))
silent := $(shell mkdir -p $(directories))

style := templates/layout.html bin/helpers.py

all: $(statics) $(indexes) $(pages)

$(statics): output/%: static/%
	cp $< $@

$(indexes): output/%: texts/% $(style)
	bin/html $< $@

$(pages): output/%/index.html: texts/%.html $(style)
	bin/html $< $@
