from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import subprocess
import os
import threading

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('frontend.html')

@app.route('/run_command', methods=['POST'])
def run_command():
    command = request.form['command'].strip()
    if command:
        if command.startswith("python detect.py"):
            # Run detection script in a separate process
            threading.Thread(target=start_detection, args=(command,), daemon=True).start()
        else:
            threading.Thread(target=execute_command, args=(command,), daemon=True).start()
        return "Command is being executed..."
    else:
        return "Please enter a command."

def execute_command(command):
    try:
        result = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        for line in result.stdout:
            socketio.emit('output', line.strip())
        result.communicate()
    except subprocess.CalledProcessError as e:
        socketio.emit('output', e.output.strip())

def start_detection(command):
    global detection_process
    detection_process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    for line in detection_process.stdout:
        socketio.emit('output', line.strip())
    detection_process.communicate()

@app.route('/stop_execution', methods=['POST'])
def stop_execution():
    global detection_process
    if detection_process and detection_process.poll() is None:
        detection_process.terminate()
        return "Execution stopped."
    else:
        return "No detection process running."

if __name__ == '__main__':
    # Set the working directory if necessary
    os.chdir(r"C:/Users/Asus/Desktop/DLCA2/yolov5-master")
    socketio.run(app, debug=True)
