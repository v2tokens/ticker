from os import chdir, getpgid, killpg, setsid
from pathlib import Path
from shlex import split
from signal import SIGTERM
from subprocess import PIPE, Popen
from time import sleep

from flask import Flask

app = Flask(__name__)

UTILS_PATH = Path("rpi-rgb-led-matrix/utils").absolute()

LED_CMD = f"sudo {UTILS_PATH}/led-image-viewer"
LED_IMG = f"{UTILS_PATH}/tipper.gif"
LED_ARGS = [
    "--led-chain=8",
    "--led-rows=32",
    "--led-cols=32",
    "--led-gpio-mapping=adafruit-hat",
]

GOAL_IMG = f"{UTILS_PATH}/TODO"

anim_proc = None
goal_proc = None


def kill_process(process):
    killpg(getpgid(process.pid), SIGTERM)


def run_animation():
    chdir(UTILS_PATH)
    cmd = split(f"{LED_CMD} {' '.join(LED_ARGS)} {LED_IMG}")
    anim_proc = Popen(cmd, preexec_fn=setsid)  # noqa


def run_goal_msg():
    chdir(UTILS_PATH)
    cmd = split(f"{LED_CMD} {' '.join(LED_ARGS)} {GOAL_IMG}")
    goal_proc = Popen(cmd, preexec_fn=setsid)  # noqa


@app.route("/")
def home():
    pass


if __name__ == "__main__":
    run_animation()
    sleep(5)
    kill_process(anim_proc)
    # app.run(debug=True, host="0.0.0.0")
