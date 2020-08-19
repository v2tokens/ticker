from os import chdir
from subprocess import run

from flask import Flask

app = Flask(__name__)


@app.route("/")
def panel():
    chdir("/home/decentral1se/rpi-rgb-led-matrix/bindings/python/samples")
    run("sudo ./runtext.py --led-cols=192 --led-rows=32", shell=True)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
