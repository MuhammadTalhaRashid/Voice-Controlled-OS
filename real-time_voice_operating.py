import whisper
import pyautogui
import pyaudio
import numpy as np
import os
import webbrowser
import time

# Load a smaller Whisper model for faster performance
model = whisper.load_model("small")

# Initialize PyAudio for real-time audio input
p = pyaudio.PyAudio()

# Parameters for real-time audio capture
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024
RECORD_SECONDS = 3
stop_command = "stop"

# Open microphone stream for audio input
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print("Listening for commands...")

# Folder navigation state
current_folder = "D:\\"

# Google typing state
google_open = False
typing_active = False

def transcribe_audio(data):
    audio = np.frombuffer(data, dtype=np.int16).astype(np.float32) / 32768.0
    result = model.transcribe(audio, language="en")
    return result["text"]

# Action functions
def open_folder(folder_name=None):
    global current_folder
    if folder_name:
        new_folder = os.path.join(current_folder, folder_name)
        if os.path.isdir(new_folder):
            current_folder = new_folder
            print(f"Navigating to folder: {current_folder}")
            os.startfile(current_folder)
        else:
            print(f"Folder '{folder_name}' does not exist in {current_folder}")
    else:
        print("Opening the current folder:", current_folder)
        os.startfile(current_folder)

def open_file(file_name):
    file_path = os.path.join(current_folder, file_name)
    
    if os.path.exists(file_path) and os.path.isfile(file_path):
        try:
            os.startfile(file_path)
            print(f"Successfully opened file: {file_path}")
        except Exception as e:
            print(f"Error: Could not open file '{file_name}'. Reason: {e}")
    else:
        print(f"File '{file_name}' does not exist in {current_folder} or is not a file.")

def open_google():
    global google_open
    if not google_open:
        print("Opening Google...")
        webbrowser.open("https://www.google.com")
        google_open = True

def start_typing():
    global typing_active
    typing_active = True
    print("Start typing activated.")

def stop_typing():
    global typing_active
    typing_active = False
    print("Stop typing activated.")

def press_key(key):
    print(f"Pressing key: {key}")
    pyautogui.press(key)

def resolution_up():
    pyautogui.hotkey("ctrl", "alt", "+")
    print("Resolution increased.")

def resolution_down():
    pyautogui.hotkey("ctrl", "alt", "-")
    print("Resolution decreased.")

def close_active_window():
    pyautogui.hotkey("alt", "f4")
    print("Closed active window.")

# New functions for full screen and half screen
def full_screen():
    pyautogui.hotkey("win", "up")
    print("Switched to full screen.")

def half_screen():
    pyautogui.hotkey("win", "down")
    print("Switched to half screen.")

def perform_action(transcription):
    global google_open, typing_active
    transcription = transcription.lower()
    
    # Folder Navigation
    if "goto folder" in transcription or "go to folder" in transcription:
        folder_name = transcription.replace("goto folder", "").replace("go to folder", "").strip()
        open_folder(folder_name)

    elif "open folder" in transcription:
        open_folder()

    # Open File Command
    elif "open file" in transcription:
        file_name = transcription.replace("open file", "").strip()
        open_file(file_name)

    # Google and Typing Commands
    elif "hey google" in transcription:
        open_google()

    elif "start typing" in transcription and google_open:
        start_typing()

    elif "stop typing" in transcription and google_open:
        stop_typing()

    # Key Press Commands
    elif "enter" in transcription:
        press_key("enter")

    elif "tab" in transcription:
        press_key("tab")

    elif "volume up" in transcription:
        pyautogui.press("volumeup", presses=5)

    elif "volume down" in transcription:
        pyautogui.press("volumedown", presses=5)

    # Resolution and Window Commands
    elif "resolution up" in transcription:
        resolution_up()

    elif "resolution down" in transcription:
        resolution_down()

    elif "close window" in transcription:
        close_active_window()

    # New Full Screen and Half Screen Commands
    elif "full screen" in transcription:
        full_screen()

    elif "half screen" in transcription:
        half_screen()

    # Stop Command
    elif "stop" in transcription:
        return "stop"
    
    else:
        print("Command not recognized. Please try again.")

buffer = b""
while True:
    print("Recording...", end="\r")
    
    audio_data = stream.read(CHUNK)
    buffer += audio_data
    
    if len(buffer) >= RATE * RECORD_SECONDS * 2:
        print("Processing transcription...", end="\r")
        transcription = transcribe_audio(buffer)
        buffer = b""
        
        print("Transcription:", transcription)
        
        # Perform action based on command first (including stop typing)
        if perform_action(transcription) == "stop":
            print("Stop command detected. Exiting...")
            break
        
        # If typing mode is active and no stop command was issued, type transcription
        if typing_active and "stop typing" not in transcription.lower():
            pyautogui.write(transcription + " ")
        
    print(" " * 50, end="\r")

# Stop the stream and close the microphone
stream.stop_stream()
stream.close()
p.terminate()


'''
"goto folder {folder name}":
Navigate to a specific folder within the current directory.

"open folder":
Opens the current folder.

"open file {file name}":
Opens a specific file from the current folder.

"hey google":
Opens Google in the browser.

"start typing":
Activates typing mode, typing spoken words until "stop typing" is issued.

"stop typing":
Deactivates typing mode.

"enter":
Simulates the Enter key press.

"tab":
Simulates the Tab key press.

"volume up":
Increases volume.

"volume down":
Decreases volume.

"resolution up":
Increases the screen resolution.

"resolution down":
Decreases the screen resolution.

"full screen"
increases the size of the window

"half screen"
decreases the size of the window

"close window":
Closes the active window or folder.

"stop":
Exits the program.
'''
