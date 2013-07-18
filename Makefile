
find = $(shell find $(1) -printf '%P\n')

statics := $(addprefix output/, $(call find, static -type f))

texts_in := $(call find, texts -name "*.html")
texts_out := $(patsubst %.html, output/%/index.html, $(texts_in))

directories := $(sort $(dir $(statics) $(texts_out)))
silent := $(shell mkdir -p $(directories))

all: $(statics) $(texts_out)

$(statics): output/%: static/%
	cp $< $@

$(texts_out): output/%/index.html: texts/%.html templates/layout.html
	bin/html $< $@
