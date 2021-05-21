# -*- encoding: utf-8 -*-
# pip install flask

import flask
from flask import request
import os
import time
import socket
import argparse

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

        print('Parsing input arguments')
        a = int(request.form['a'])
        b = int(request.form['b'])
        print('Running ' + MATLAB_FUNCTION + '(' + str(a) + ',' + str(b) + ')')
        # FOR WINDOWS
        #answer = os.popen( MATLAB_PATH +  ' -sd ' + MATLAB_SCRIPT_FOLDER + ' -batch ' + MATLAB_FUNCTION + '(' + str(a) + ',' + str(b) + ')').read()

        # FOR LINUX
        answer = os.popen( MATLAB_PATH +  ' -nodisplay -batch "cd(\'' + MATLAB_SCRIPT_FOLDER + '\');' + MATLAB_FUNCTION + '(' + str(a) + ',' + str(b) + ')' + '"').read()
        print('Sending Matlab answer: ' + answer)
        response_list = [("matlab_answer", answer)]

        response_dict = dict(response_list)

        return flask.jsonify(response_dict)

    except Exception as err:
        print("ko:", err)

    return "ok"



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Server for running Matlab script')
    parser.add_argument("--matlab_path",
                        required = True,
                        help = "Path to the matlab.exe")
    parser.add_argument("--matlab_script_folder",
                        required = True,
                        help = "Path to the folder containing the .m file")
    parser.add_argument("--matlab_function",
                        required = True,
                        help = "Name of the Matlab function to run")


    args = parser.parse_args()

    global MATLAB_PATH
    MATLAB_PATH = args.matlab_path

    global MATLAB_SCRIPT
    MATLAB_SCRIPT_FOLDER = args.matlab_script_folder

    global MATLAB_FUNCTION
    MATLAB_FUNCTION = args.matlab_function

    IP = socket.gethostbyname(socket.gethostname())
    app.run(port = 9099, host = IP)


