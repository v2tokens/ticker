URL     := https://github.com/hzeller/rpi-rgb-led-matrix
CLONED  := rpi-rgb-led-matrix
DEPS    := python3-dev libgraphicsmagick++-dev libwebp-dev

default: server

deps:
	@sudo apt-get update && sudo apt-get install $(DEPS) -y

clone:
	@git clone $(URL)

build:
	@cd $(CLONED)/utils && make led-image-viewer

install: deps clone build
	@python3 -m venv .venv && \
	.venv/bin/pip install -r requirements.txt

server:
	@.venv/bin/python3 app.py

.PHONY: deps clone build install server
