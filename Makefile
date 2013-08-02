# Custom "find" command that returns files names without the leading
# directory name, so that we can supplement them simply with "addprefix"
# instead of having to do a full "patsubst" on them.

find = $(shell find $(1) -printf '%P\n')

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
silent := $(shell mkdir -p $(directories))

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
