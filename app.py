from os import chdir, kill, setsid, getpgid, killpg
from signal import SIGKILL, SIGTERM
from pathlib import Path
from shlex import split
from subprocess import Popen, PIPE
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


def run_animation():
    chdir(UTILS_PATH)
    cmd = f"{LED_CMD} {' '.join(LED_ARGS)} {LED_IMG}"
    result = Popen(split(cmd), stdout=PIPE, stderr=PIPE, preexec_fn=setsid) 
    sleep(5)
    killpg(getpgid(result.pid), SIGTERM)


def run_goal_msg():
    pass


animations_process = None 
goal_message_process = None 


@app.route("/")
def home():
    pass


if __name__ == "__main__":
    run_animation()
    # app.run(debug=True, host="0.0.0.0")
