# -*- encoding: utf-8 -*-
# pip install flask

import flask
from flask import request
import os
import time
import socket
import argparse
import base64

from PIL import Image
from io import BytesIO
import numpy as np

app = flask.Flask(__name__)

folder = ""

# Configure the flask server
app.config['JSON_SORT_KEYS'] = False
global MATLAB_PATH
global MATLAB_SCRIPT_FOLDER
global MATLAB_FUNCTION


@app.route("/api/matlab_run_cmd", methods=['POST'])
def api_matlab_run_cmd():
    try:
        global MATLAB_PATH
        global MATLAB_SCRIPT_FOLDER
        global MATLAB_FUNCTION

        print('Parsing input ... ')
        img = request.data

        print("image data received!")
        decodeit = open('image2.jpg', 'wb')
        conv_img = base64.b64decode((img))
        decodeit.write(conv_img)
        decodeit.close()

        print('Running transformation processes on image ...')
        img2_rotation = image_rotation('image2.jpg')
        img2_rotation.show()

        print("sending response back:")
        ans = "Image sucessfuly recieved! "

        return ans

    except Exception as err:
        print("ko:", err)

    return "ok"


def image_rotation(image_name):

    image = Image.open(image_name)
    rotated = image.rotate(45)
    # image.show()

    return rotated


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Server for running Matlab script')
    parser.add_argument("--matlab_path",
                        required=True,
                        help="Path to the matlab.exe")
    parser.add_argument("--matlab_script_folder",
                        required=True,
                        help="Path to the folder containing the .m file")
    parser.add_argument("--matlab_function",
                        required=True,
                        help="Name of the Matlab function to run")

    args = parser.parse_args()

    global MATLAB_PATH
    MATLAB_PATH = args.matlab_path

    global MATLAB_SCRIPT
    MATLAB_SCRIPT_FOLDER = args.matlab_script_folder

    global MATLAB_FUNCTION
    MATLAB_FUNCTION = args.matlab_function

    IP = socket.gethostbyname(socket.gethostname())
    app.run(port=9099, host=IP)
