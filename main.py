import lib.aes as aes
import os,re, json, sys
import requests, webview
from functools import wraps
from flask import Flask, jsonify, render_template, request

gui_dir = os.path.join(os.path.dirname(__file__), 'gui')
src_dir = os.path.join(os.path.dirname(__file__), 'gui/assets')

if not os.path.exists(gui_dir):
    gui_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gui')

server = Flask(__name__, static_folder=src_dir, template_folder=gui_dir)
server.config['SEND_FILE_MAX_AGE_DEFAULT'] = 1

def verify_token(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        data = json.loads(request.data)
        token = data.get('token')
        if token == webview.token:
            return function(*args, **kwargs)
        else:
            raise Exception('Authentication error')
    return wrapper

@server.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store'
    return response

@server.route('/')
def landing():
    """
    render index.html 
    """
    return render_template('index.html', token=webview.token)


@server.route('/upload', methods=['POST'])
def select():
    """
    create the directory dialog using webview (FOLDER_DIALOG for selecting directories)
    """

    directory = webview.windows[0].create_file_dialog(webview.FOLDER_DIALOG)
    
    if directory:
        return jsonify({'status': 'success', 'path': directory[0]})
    else:
        return jsonify({'status': 'cancel'})

@server.route('/process', methods=['POST'])
def process():
    """
    Process and encrypt/decrypt files with AES algorithm.
    """
    data = request.json
    mode = data.get('mode')
    password = data.get("key")
    directory = data.get('dir')

    if not os.path.isdir(directory):
        return jsonify({'status': 'error', 'output': 'directory not found.'})

    files_count = sum(len(files) for _, _, files in os.walk(directory))

    if files_count == 0:
        return jsonify({'status': 'error', 'output': 'directory is empty.'})

    proccessed = aes.crypter(mode, directory, password)

    if isinstance(proccessed, str):
        return jsonify({'status': 'error', 'output': proccessed})

    return jsonify({'status': 'success', 'output': f"{proccessed} files {mode}ed successfully."})

def main():
    window = webview.create_window('tufe | gui', server, resizable=False)
    if sys.platform == "linux" or sys.platform == "linux2": webview.start(gui='qt')
    else: webview.start()

if __name__ == '__main__': main()
