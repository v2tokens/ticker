URL     := https://github.com/hzeller/rpi-rgb-led-matrix
CLONED  := rpi-rgb-led-matrix
DEPS    := python3-dev


deps:
	@sudo apt-get update && sudo apt-get install $(DEPS) -y

clone:
	@git clone $(URL)

build:
	@cd $(CLONED) && \
	make build-python PYTHON=/usr/bin/python3 && \
	sudo make install-python PYTHON=/usr/bin/python3

install: build
	@python3 -m venv .venv && \
	.venv/bin/pip install -r requirements.txt

server:
	@.venv/bin/python3 app.py

gifs:
	@cp gifs/* $(CLONED)/utils/

.PHONY: deps clone build install server gifs
