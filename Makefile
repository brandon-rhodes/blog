
all:

statics_in := $(shell find static -type f)
statics_out := $(subst static/, output/, $(statics_in))

$(statics_out): output/%: static/%
	cp $< $@

all: $(statics_out)

texts_in := $(shell find texts -name "*.html")
texts_out := $(subst texts/, output/, $(texts_in))

$(texts_out): output/%.html: texts/%.html templates/layout.html
	bin/html $< $@

all: $(texts_out)

posts := $(wildcard _posts/*.rst)

foo.txt: $(posts)
	echo "$+" > foo.txt
