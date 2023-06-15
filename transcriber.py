import sys
import speech_recognition as sr
import tkinter as tk
from tkinter import filedialog
from datetime import datetime
import threading

# Variáveis globais para controlar o estado do botão e a transcrição
listening = False
transcription = ""

def transcribe_audio():
    global listening, transcription

    # Create a recognizer object
    r = sr.Recognizer()

    # Set the microphone as the audio source
    mic = sr.Microphone()

    # Adjust the microphone for ambient noise
    with mic as source:
        print("Adjusting microphone for ambient noise...")
        r.adjust_for_ambient_noise(source)

    listening = True

    # Start listening to the microphone
    print("Listening...")
    with mic as source:
        while listening:
            audio = r.listen(source)

            try:
                # Perform speech recognition
                print("Transcribing...")
                transcription += r.recognize_google(audio) + " "
                print("Transcription:", transcription)
            except sr.UnknownValueError:
                print("Speech recognition could not understand audio")
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))

def save_transcription():
    global transcription

    # Get the password from the user
    password = password_entry.get()

    # Check if the password is correct
    if password == "JHG9ner45987!*":
        # Append the transcription to the output file
        with open("output.txt", "a") as file:
            file.write(transcription + "\n")

        print("Transcription saved.")
    else:
        print("Incorrect password. Transcription not saved.")

def stop_listening():
    global listening
    listening = False
    save_transcription()
    print("Transcription stopped.")

def start_transcription():
    # Disable the Transcribe button and enable the Stop button
    transcribe_btn.config(state=tk.DISABLED)
    stop_btn.config(state=tk.NORMAL)

    # Start the audio transcription in a new thread
    thread = threading.Thread(target=transcribe_audio)
    thread.start()

def create_gui():
    # Create the GUI
    global transcribe_btn, stop_btn, password_entry

    window = tk.Tk()
    window.title("Audio Transcription by Felipe - Wella ")
    window.geometry("300x250")

    transcribe_btn = tk.Button(window, text="Transcribe", command=start_transcription)
    transcribe_btn.pack(pady=20)

    stop_btn = tk.Button(window, text="Stop", command=stop_listening, state=tk.DISABLED)
    stop_btn.pack(pady=10)

    password_label = tk.Label(window, text="Password:")
    password_label.pack()

    password_entry = tk.Entry(window, show="*")
    password_entry.pack()

    window.mainloop()

def exit_program():
    sys.exit()

create_gui()
exit_program()
