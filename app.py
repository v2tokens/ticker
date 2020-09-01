from os import chdir, getpgid, killpg, setsid
from pathlib import Path
from shlex import split
from signal import SIGTERM
from subprocess import Popen

from flask import Flask, jsonify

app = Flask(__name__)

anim_proc = None
goal_proc = None

ROOT_PATH = Path(".").absolute()
UTILS_PATH = Path("rpi-rgb-led-matrix/utils").absolute()

LED_CMD = "./led-image-viewer"
LED_ARGS = " ".join(
    [
        "--led-chain=8",
        "--led-rows=32",
        "--led-cols=32",
        "--led-parallel=1",
        "--led-gpio-mapping=adafruit-hat",
        "--led-brightness=80",
        "--led-pwm-bits=5",
        "--led-no-hardware-pulse",
        "--led-slowdown-gpio=3",
    ]
)

ANIM_IMGS = " ".join(
    [
        "../../gifs/bongacams_scroller_1.gif",
        "../../gifs/bongacams_scroller_2.gif",
        "../../gifs/chaturbate_01.gif",
    ]
)
ANIM_CMD = split(f"{LED_CMD} {LED_ARGS} -f -s {ANIM_IMGS}")


GOAL_IMG = "../../gifs/Goal_reached.gif"
GOAL_CMD = split(f"{LED_CMD} {LED_ARGS} -t 20 {GOAL_IMG}")


def kill_process(process):
    killpg(getpgid(process.pid), SIGTERM)


def run_led(cmd):
    chdir(UTILS_PATH)
    process = Popen(cmd, preexec_fn=setsid)
    chdir(ROOT_PATH)
    return process


@app.route("/ok")
def isup():
    return jsonify(success=True)


@app.route("/")
def home():
    global anim_proc
    global goal_proc

    # Note(decentral1se): Return early if we're already showing the message
    if goal_proc and goal_proc.poll() is None:
        return jsonify(success=True)

    if anim_proc:
        kill_process(anim_proc)

    goal_proc = run_led(GOAL_CMD)

    # Note(decentral1se): opportunistically re-run the animations which take
    # much longer to load so as to arrange them to show in a timely fashion
    anim_proc = run_led(ANIM_CMD)

    return jsonify(success=True)


if __name__ == "__main__":
    anim_proc = run_led(ANIM_CMD)

    try:
        app.run(debug=False, host="0.0.0.0")
    finally:
        if anim_proc:
            kill_process(anim_proc)
        if goal_proc:
            kill_process(goal_proc)
