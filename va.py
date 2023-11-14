import sys
import threading
import tkinter as tk

import speech_recognition
import pyttsx3 as tts

from neuralintents import BasicAssistant

class Assistant:
    def __init__(self):
        self.recognizer = speech_recognition.Recognizer()
        self.speaker = tts.init()
        self.speaker.setProperty("rate", 150)

        intents_data = {
            "intents": [
                {
                    "tag": "greeting",
                    "patterns": ["Hi", "Hey", "What's up?", "Hey how are you doing"],
                    "responses": ["Hey", "What can I do for you?"],
                },
                {
                    "tag": "neuralnine",
                    "patterns": ["What is NeuralNine", "Tell me about NeuralNine", "Who is NeuralNime"],
                    "responses": ["NeuralNine is a youtube channel and an online brand, which focuses on programming, machine learning and other new technologies."],
                },
                {
                    "tag": "name",
                    "patterns": ["What is your name?", "What should I call you", "Can I know your name?"],
                    "responses": ["My name is Jarvis!"],
                },
                {
                    "tag": "file",
                    "patterns": ["Create a file", "Create a new file"],
                    "responses": ["Sure, I'll create a file for you.", "Creating a new file. Done!", "A new file has been created."],
                },
            ]
        }

        self.assistant = BasicAssistant(intents_data)
        self.root = tk.Tk()
        self.label = tk.Label(text="🤖", font=("Arial", 120, "bold"))
        self.label.pack()

        threading.Thread(target=self.run_assistant).start()

        self.root.mainloop()

    def run_assistant(self):
        while True:
            try:
                with speech_recognition.Microphone() as mic:
                    self.recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                    audio = self.recognizer.listen(mic)

                    text = self.recognizer.recognize_google(audio)
                    text = text.lower()

                    if "hey Jarvis" in text:
                        self.label.config(fg="blue")
                        audio = self.recognizer.listen(mic)
                        text = self.recognizer.recognize_google(audio)
                        text = text.lower()
                        if text == "stop":
                            self.speaker.say("Bye")
                            self.speaker.runAndWait()
                            self.speaker.stop()
                            self.root.destroy()
                            sys.exit()
                        else:
                            if text is not None:
                                response = self.assistant.request(text)
                                if response is not None:
                                    self.speaker.say(response)
                                    self.speaker.runAndWait()
                                self.label.config(fg="black")

            except Exception as e:
                print(f"An error occurred: {e}")
                self.label.config(fg="black")
                continue

Assistant()
