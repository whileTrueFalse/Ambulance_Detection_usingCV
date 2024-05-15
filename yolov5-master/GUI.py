import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
import subprocess
import os
import threading

def run_command():
    command = command_entry.get("1.0",'end-1c').strip()
    if command:
        if command.startswith("python detect.py"):
            # Run detection script in a separate process
            threading.Thread(target=start_detection, args=(command,), daemon=True).start()
        else:
            threading.Thread(target=execute_command, args=(command,), daemon=True).start()
    else:
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, "Please enter a command.")

def execute_command(command):
    try:
        result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, result)
    except subprocess.CalledProcessError as e:
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, e.output)

def start_detection(command):
    global detection_process
    detection_process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # Read output of the process and display in the UI
    for line in iter(detection_process.stdout.readline, b''):
        output_text.insert(tk.END, line.decode())
    detection_process.wait()

import signal

def stop_execution():
    global detection_process
    if 'detection_process' in globals() and detection_process is not None:
        os.kill(detection_process.pid, signal.CTRL_C_EVENT)  # Send KeyboardInterrupt signal
        detection_process = None
    else:
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, "No detection process running.")



# Set the working directory if necessary
os.chdir(r"C:\Users\Asus\Desktop\DLCA2\yolov5-master")

# Create main window
root = tk.Tk()
root.title("SAVED")

# Set background color to black and text color to green
root.configure(bg="black")
root.option_add("*TCombobox*Listbox*background", "black")
root.option_add("*TCombobox*Listbox*foreground", "green")

# Load a theme
import ttkthemes
style = ttkthemes.ThemedStyle(root)
style.set_theme("radiance")

# Header Label
header_label = ttk.Label(root, text="Smart Ambulance Vehicle Detection", font=("Segoe UI", 24, "bold"), foreground="#03fc39", background="black")
header_label.pack(pady=20)

# Command Entry
command_label = ttk.Label(root, text="Enter command:", font=("Segoe UI", 14), background="black", foreground="green")
command_label.pack()
command_entry = ScrolledText(root, height=10, width=70, font=("Segoe UI", 12), bg="black", fg="green")
command_entry.pack(pady=5)

# Output Text
output_label = ttk.Label(root, text="Output:", font=("Segoe UI", 14), background="black", foreground="green")
output_label.pack()
output_text = ScrolledText(root, height=15, width=70, font=("Segoe UI", 12), bg="black", fg="green")
output_text.pack(pady=5)

import subprocess

if __name__ == "__main__":
    cmd = ['cmd', '/c', 'dir']  # Use 'cmd' to run 'dir' command on Windows
    result = subprocess.run(cmd, capture_output=True, text=True, check=False)
    print(result)
    print(result.stdout)

# Run Button
run_button = ttk.Button(root, text="Run Command", command=run_command, style="Accent.TButton")
run_button.pack(pady=10)

# Stop Button
stop_button = ttk.Button(root, text="Stop Execution", command=stop_execution, style="Danger.TButton")
stop_button.pack(pady=10)

# Status Bar
status_bar = ttk.Label(root, text="Ready", relief=tk.SUNKEN, anchor=tk.W, background="black", foreground="green")
status_bar.pack(side=tk.BOTTOM, fill=tk.X)

# Function to update status bar
def update_status(status):
    status_bar.config(text=status)

# Bind Return key to run_command function
root.bind('<Return>', lambda event=None: run_command())

# Start GUI
root.mainloop()
