path    := PATH=./vendor/python/bin:$(shell echo "${PATH}")
version := $(shell $(path) python setup.py --version)
name    := $(shell $(path) python setup.py --name)
dist    := dist/$(name)-$(version).tar.gz

#################################################
#
# Build the pip package
#
#################################################

build: $(dist)

$(dist): $(shell find biobox) requirements.txt setup.py
	$(path) python setup.py sdist
	touch $@

#################################################
#
# Bootstrap project requirements for development
#
#################################################

bootstrap: vendor/python

vendor/python: requirements.txt
	mkdir -p log
	virtualenv $@ 2>&1 > log/virtualenv.txt
	$(path) pip install -r $< 2>&1 > log/pip.txt
	touch $@

.PHONY: bootstrap
