import speech_recognition as sr
import pyttsx3
import threading

class VoiceModule:
    def __init__(self, gui):
        self.gui = gui

        # Speech-to-Text setup
        self.r = sr.Recognizer()
        self.r.energy_threshold = 300
        self.r.dynamic_energy_threshold = True
        self.is_listening = False

        # Text-to-Speech setup
        self.engine = pyttsx3.init('sapi5')
        
    def start_speech_to_text(self):
        if self.is_listening:
            return

        self.is_listening = True
        self.gui.update_status("Listening... Speak now")
        threading.Thread(target=self._listen_to_speech, daemon=True).start()

    def _listen_to_speech(self):
        with sr.Microphone() as source:
            self.r.adjust_for_ambient_noise(source, duration=1)
            while self.is_listening:
                try:
                    audio = self.r.listen(source, timeout=5, phrase_time_limit=10)
                    text = self.r.recognize_google(audio)
                    self.gui.text_area.insert("end", text + " ")
                    self.gui.update_status(f"Recognized: {text}")
                except sr.UnknownValueError:
                    self.gui.update_status("Could not understand audio")
                except Exception as e:
                    self.gui.update_status(f"Error: {str(e)}")
                    break

    def stop_speech_to_text(self):
        self.is_listening = False
        self.gui.update_status("Stopped listening")

    def start_text_to_speech(self):
        text = self.gui.text_area.get("1.0", "end").strip()
        if not text:
            self.gui.update_status("No text to read")
            return

        self.gui.update_status("Reading text...")
        threading.Thread(target=self._speak_text, args=(text,), daemon=True).start()

    def _speak_text(self, text):
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[0].id)
        self.engine.setProperty('rate', 170)
        self.engine.setProperty('volume', 0.9)

        self.engine.say(text)
        try:
            self.engine.runAndWait()
            self.gui.update_status("Finished reading")
        except Exception as e:
            self.gui.update_status(f"Error in reading: {str(e)}")

    def stop_text_to_speech(self):
        self.engine.stop()
        self.gui.update_status("Stopped reading")