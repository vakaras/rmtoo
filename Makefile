.PHONY: all
all: reqtree.png doc/latex2/requirements.pdf

#
# This is the way the rmtoo must be called.
#
CALL_RMTOO=./bin/rmtoo -m . -f doc/requirements/Config3.py -d doc/requirements

#
# Dependency handling
#  The file .rmtoo_dependencies is created by rmtoo itself.
#
include .rmtoo_dependencies

# And how to make the dependencies
.rmtoo_dependencies:
	./bin/rmtoo -m . -f doc/requirements/Config3.py \
		-d doc/requirements \
		--create-makefile-dependencies=.rmtoo_dependencies

reqtree.png: reqtree.dot
	dot -Tpng -o reqtree.png reqtree.dot

# Two calls are needed: one for the requirments converting and one for
# backlog creation.
doc/latex2/requirements.pdf: ${REQS_LATEX2} doc/latex2/requirements.tex
	(cd doc/latex2 && \
	   gnuplot ../../contrib/gnuplot_stats_reqs_cnt.inc && \
	   epstopdf stats_reqs_cnt.eps)
	(cd doc/latex2 && pdflatex requirements.tex; \
		pdflatex requirements.tex; \
		pdflatex requirements.tex)

.PHONY: clean
clean:
	rm -f reqtree.dot reqtree.png doc/latex2/reqtopics.tex \
		doc/latex2/requirements.aux doc/latex2/requirements.dvi \
		doc/latex2/requirements.log doc/latex2/requirements.out \
		doc/latex2/requirements.pdf doc/latex2/requirements.toc 
	rm -fr debian/rmtoo build

PYSETUP = python setup.py

.PHONY: install
install:
	$(PYSETUP) install --prefix=${DESTDIR}/usr \
		--install-scripts=${DESTDIR}/usr/bin

.PHONY: tests
tests:
	nosetests -w rmtoo -v --with-coverage -s --cover-package=rmtoo

.PHONY: deb
deb:
	debuild -I -Imake_latex.log
