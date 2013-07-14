
statics_in := $(shell find static -type f)
statics_out := $(subst static/, output/, $(statics_in))

texts_in := $(shell find texts -name "*.html")
texts_out := $(subst texts/, output/, $(texts_in))

directories := $(sort $(dir $(statics_out) $(texts_out)))
silent := $(shell mkdir -p $(directories))

all: $(statics_out) $(texts_out)

$(statics_out): output/%: static/%
	cp $< $@

$(texts_out): output/%.html: texts/%.html templates/layout.html
	bin/html $< $@
