from multiprocessing import Process
from os import chdir
from pathlib import Path
from shlex import split
from subprocess import run

from flask import Flask

app = Flask(__name__)

UTILS_PATH = Path("rpi-rgb-led-matrix/utils").absolute()

LED_CMD = f"{UTILS_PATH}/led-image-viewer"
LED_IMG = f"{UTILS_PATH}/chaturbate.ppm"
LED_ARGS = [
    "--led-chain=8",
    "--led-rows=32",
    "--led-cols=32",
    "--led-parallel=1",
    "--led-gpio-mapping=adafruit-hat",
    "-f",
]


def run_animation():
    chdir(UTILS_PATH)
    cmd = f"{LED_CMD} {" ".join(LED_ARGS)} {LED_IMG}"
    run(split(cmd))


def run_goal_msg():
    pass


animations_process = Process(target=run_animation)
goal_message_process = Process(target=run_goal_msg)


@app.route("/")
def home():
    pass


if __name__ == "__main__":
    animations_process.start()
    # app.run(debug=True, host="0.0.0.0")
