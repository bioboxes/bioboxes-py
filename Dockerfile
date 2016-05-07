FROM alpine:3.3

ENV install apk add --no-cache

RUN apk update && ${install} \
	bash \
	g++ \
	libffi-dev \
	openssl-dev \
	py-pip \
	python \
	python-dev
