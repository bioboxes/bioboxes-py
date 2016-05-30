path    := PATH=.tox/py27/bin:$(shell echo "${PATH}")
version := $(shell $(path) python setup.py --version)
name    := $(shell $(path) python setup.py --name)
dist    := dist/$(name)-$(version).tar.gz

installer-image := test-install

#################################################
#
# Publish the pip package
#
#################################################

publish: $(dist)
	@$(path) twine upload \
		--username ${PYPI_USERNAME} \
		--password ${PYPI_PASSWORD} \
		$^

#################################################
#
# Build the pip package
#
#################################################

build: $(dist) test-build

test-build: $(dist)
	docker run \
		--tty \
		--volume=$(abspath $(dir $^)):/dist:ro \
		$(installer-image) \
		/bin/bash -c "pip install --user /$^"

$(dist): $(shell find biobox) requirements/default.txt setup.py MANIFEST.in
	$(path) python setup.py sdist
	touch $@

#################################################
#
# Unit tests
#
#################################################

test     = tox
autotest = clear && $(test) -- -m \'not slow\'

test:
	@$(test)

autotest:
	@$(autotest) || true # Using true starts tests even on failure
	@fswatch \
		--exclude 'pyc' \
		--one-per-batch	./biobox \
		--one-per-batch ./test \
		| xargs -n 1 -I {} bash -c "$(autotest)"

#################################################
#
# Bootstrap project requirements for development
#
#################################################

bootstrap: .tox tmp/data/reads.fq.gz .$(installer-image)
	mkdir -p ./tmp/tests
	docker pull bioboxes/velvet@sha256:6611675a6d3755515592aa71932bd4ea4c26bccad34fae7a3ec1198ddcccddad
	docker pull alpine:3.3
	docker pull alpine@sha256:9cacb71397b640eca97488cf08582ae4e4068513101088e9f96c9814bfda95e0

.$(installer-image): Dockerfile
	docker build --tag $(installer-image) .
	touch $@

.tox: requirements/default.txt requirements/development.txt
	tox --notest
	@touch $@

tmp/data/reads.fq.gz:
	@mkdir -p $(dir $@)
	@wget \
		--quiet \
		--output-document $@ \
		https://s3-us-west-1.amazonaws.com/nucleotides-testing/short-read-assembler/reads.fq.gz


.PHONY: bootstrap build test
