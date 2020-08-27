URL     := https://github.com/hzeller/rpi-rgb-led-matrix
CLONED  := rpi-rgb-led-matrix
DEPS    := python3-dev python3-pillow
MATRIX  := rpi-rgb-led-matrix
PYFILES := base.py tipper.py


default: matrix 

deps:
	@sudo apt-get update && sudo apt-get install $(DEPS) -y

clone:
	@git clone $(URL)

build:
	@cd $(CLONED) && \
	make build-python PYTHON=/usr/bin/python3 && \
	sudo make install-python PYTHON=/usr/bin/python3

matrix: build

format:
	@black $(PYFILES)

.PHONY: deps clone build 
