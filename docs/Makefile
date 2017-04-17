# Makefile for Sphinx documentation
#

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
PAPER         =
BUILDDIR      = _build

# Internal variables.
ALLSPHINXOPTS   = -d $(BUILDDIR)/doctrees $(PAPEROPT_$(PAPER)) $(SPHINXOPTS) .

.PHONY: help clean html dirhtml singlehtml livehtml

clean:
	-rm -rf $(BUILDDIR)/*

rm-crud:
	@find . -name .#* -delete
	@find . -name ._* -delete

html: rm-crud
	$(SPHINXBUILD) -b html $(ALLSPHINXOPTS) $(BUILDDIR)/html

coverage: rm-crud
	$(SPHINXBUILD) -b coverage $(ALLSPHINXOPTS) $(BUILDDIR)/coverage

livehtml: html
	livereload $(BUILDDIR)/html -p 33234

dirhtml: rm-crud
	$(SPHINXBUILD) -b dirhtml $(ALLSPHINXOPTS) $(BUILDDIR)/dirhtml

singlehtml: rm-crud
	$(SPHINXBUILD) -b singlehtml $(ALLSPHINXOPTS) $(BUILDDIR)/singlehtml

# cp README_build.md $(BUILDDIR)/html/README.md
deploy: clean html
	git fetch origin
	ghp-import -n -p -r origin -b gh-pages $(BUILDDIR)/html