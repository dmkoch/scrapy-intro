# Makefile for presentation, uses cleaver: https://github.com/jdan/cleaver
OBJDIR := build

all: $(OBJDIR)/presentation.html $(OBJDIR)/spidercat.jpg

$(OBJDIR):
	mkdir -p $@

$(OBJDIR)/presentation.html:
	cleaver presentation.md

$(OBJDIR)/spidercat.jpg:
	cp spidercat.jpg $(OBJDIR)

$(OBJDIR)/presentation.html: | $(OBJDIR)

$(OBJDIR)/spidercat.jpg: | $(OBJDIR)

clean:
	rm -rf build
