from os import chdir, getpgid, killpg, setsid
from pathlib import Path
from shlex import split
from signal import SIGTERM
from subprocess import Popen
from time import sleep

from flask import Flask, jsonify

app = Flask(__name__)

anim_proc = None

ROOT_PATH = Path(".").absolute()
UTILS_PATH = Path("rpi-rgb-led-matrix/utils").absolute()

LED_CMD = f"sudo {UTILS_PATH}/led-image-viewer"
LED_IMG = f"{UTILS_PATH}/tipper.gif"
LED_ARGS = [
    "--led-chain=8",
    "--led-rows=32",
    "--led-cols=32",
    "--led-gpio-mapping=adafruit-hat",
]

GOAL_IMG = f"{UTILS_PATH}/bonga.gif"


def kill_process(process):
    killpg(getpgid(process.pid), SIGTERM)


def run_animation():
    chdir(UTILS_PATH)
    cmd = split(f"{LED_CMD} {' '.join(LED_ARGS)} {LED_IMG}")
    process = Popen(cmd, preexec_fn=setsid)
    chdir(ROOT_PATH)
    return process


def run_goal_msg():
    chdir(UTILS_PATH)
    cmd = split(f"{LED_CMD} {' '.join(LED_ARGS)} -t 3 {GOAL_IMG}")
    process = Popen(cmd, preexec_fn=setsid)
    chdir(ROOT_PATH)
    return process


@app.route("/")
def home():
    global anim_proc

    kill_process(anim_proc)

    goal_proc = run_goal_msg()
    goal_proc.wait()

    anim_proc = run_animation()

    return jsonify(success=True)


if __name__ == "__main__":
    anim_proc = run_animation()
    app.run(debug=False, host="0.0.0.0")
