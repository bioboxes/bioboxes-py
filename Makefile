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

$(dist): $(shell find biobox) requirements/default.txt setup.py
	$(path) python setup.py sdist
	touch $@

#################################################
#
# Unit tests
#
#################################################

test     = $(path) python -m pytest --ignore=./vendor
autotest = clear && $(test) -m 'not slow'

test:
	@$(test)

autotest:
	@$(autotest) || true # Using true starts tests even on failure
	@fswatch -o ./biobox -o ./test | xargs -n 1 -I {} bash -c "$(autotest)"

#################################################
#
# Bootstrap project requirements for development
#
#################################################

bootstrap: vendor/python
	docker pull alpine:3.3

vendor/python: requirements/default.txt requirements/development.txt
	mkdir -p log
	virtualenv $@ 2>&1 > log/virtualenv.txt
	$(path) pip install \
		--requirement requirements/default.txt \
		--requirement requirements/development.txt \
		2>&1 > log/pip.txt
	touch $@

tmp/data/reads.fq.gz:
	mkdir -p $(dir $@)
	wget \
		--quiet \
		--output-document $@ \
		https://s3-us-west-1.amazonaws.com/nucleotides-testing/short-read-assembler/reads.fq.gz


.PHONY: bootstrap build test
