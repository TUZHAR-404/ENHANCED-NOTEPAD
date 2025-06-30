import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import customtkinter as ctk
import pyttsx3                                                           #adding all necessory tech
import speech_recognition as sr
import threading
import pyaudio
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.animation import FuncAnimation



class NotepadApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Audio Notepad with 3D Visuals")
        self.root.geometry("1200x800")                                                      # main gui
        self.audio_settings = {
            'tts_volume': 1.0,
            'tts_rate': 150,                                                             # Audio settings
            'tts_voice': 0,
            'stt_energy_threshold': 300,
            'stt_device_index': None
        }
        self.visualization_active = False                                              # Visualization settings
        self.animation = None
        
        ctk.set_appearance_mode("system")                                                 # next time change it to RGB after exam
        ctk.set_default_color_theme("blue")
        
        self.current_file = None
        self.is_listening = False
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.audio = pyaudio.PyAudio()
        self.setup_audio_devices()
        self.create_widgets()
        
    def setup_audio_devices(self):
        self.input_devices = []
        for i in range(self.audio.get_device_count()):                                           # AUDIO I/O
            dev_info = self.audio.get_device_info_by_index(i)
            if dev_info['maxInputChannels'] > 0:
                self.input_devices.append((i, dev_info['name']))

        self.tts_voices = []
        voices = self.engine.getProperty('voices')                                     #adding voices
        for i, voice in enumerate(voices):
            self.tts_voices.append((i, voice.name))
    
    def create_3d_visualization(self):
        if self.visualization_active:                                         #USING AI TO MAKE 3D ANIMATION
            return
            
        self.visualization_active = True
        self.visualization_frame = ctk.CTkFrame(self.right_frame)
        self.visualization_frame.pack(expand=True, fill="both", padx=5, pady=5)

        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.ax = self.fig.add_subplot(111, projection='3d')
    
        u = np.linspace(0, 2 * np.pi, 100)
        v = np.linspace(0, np.pi, 100)
        self.x = np.outer(np.cos(u), np.sin(v))                             # CREATING SPHERE BY USING AI
        self.y = np.outer(np.sin(u), np.sin(v))
        self.z = np.outer(np.ones(np.size(u)), np.cos(v))
        
        self.sphere = self.ax.plot_surface(
            self.x, self.y, self.z,
            facecolors=self.calculate_rgb_colors(self.x, self.y, self.z),
            rstride=4, cstride=4, shade=False
        )
        self.ax.set_axis_off()
        self.ax.set_xlim([-1.5, 1.5])
        self.ax.set_ylim([-1.5, 1.5])
        self.ax.set_zlim([-1.5, 1.5])
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.visualization_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(expand=True, fill="both")
        
 
        self.animation = FuncAnimation(
            self.fig, self.update_animation,
            frames=100, interval=50, blit=False
        )
    
    def calculate_rgb_colors(self, x, y, z):
        r = (x + 1) / 2
        g = (y + 1) / 2
        b = (z + 1) / 2
        return np.dstack((r, g, b))
    
    def update_animation(self, frame):
        # Rotate the sphere
        angle = np.radians(frame * 3.6)  # 360 degrees over 100 frames
        x_new = self.x * np.cos(angle) - self.y * np.sin(angle)
        y_new = self.x * np.sin(angle) + self.y * np.cos(angle)
        z_new = self.z
        
        # Update sphere data
        self.sphere.remove()
        self.sphere = self.ax.plot_surface(
            x_new, y_new, z_new,
            facecolors=self.calculate_rgb_colors(x_new, y_new, z_new),
            rstride=4, cstride=4, shade=False
        )
        
        return self.sphere,
    
    def remove_3d_visualization(self):
        if not self.visualization_active:
            return
            
        if self.animation:
            self.animation.event_source.stop()
        
        if hasattr(self, 'visualization_frame'):
            self.visualization_frame.destroy()
            del self.visualization_frame
            
        self.visualization_active = False
    
    def create_widgets(self):
        self.main_frame = ctk.CTkFrame(self.root)                                             # MAIN WORK STARTS FROM HERE
        self.main_frame.pack(expand=True, fill="both", padx=5, pady=5)

        self.left_frame = ctk.CTkFrame(self.main_frame)
        self.left_frame.pack(side="left", expand=True, fill="both", padx=5, pady=5)
 
        self.right_frame = ctk.CTkFrame(self.main_frame, width=400)
        self.right_frame.pack(side="right", fill="both", padx=5, pady=5)
        self.right_frame.pack_propagate(False)
        

        self.menu_bar = tk.Menu(self.root)                                                      #MAIN STUFF CREATING LIKE MENU,ETC
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="New", command=self.new_file, accelerator="Ctrl+N")
        self.file_menu.add_command(label="Open", command=self.open_file, accelerator="Ctrl+O")          # WIDGETS
        self.file_menu.add_command(label="Save", command=self.save_file, accelerator="Ctrl+S")
        self.file_menu.add_command(label="Save As", command=self.save_file_as)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.exit_app)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        
        # Edit menu TO EDIT OR ADD CHANGES ON NOT_UR_AVG_NOTEPAD:)
        self.edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.edit_menu.add_command(label="Cut", command=self.cut_text, accelerator="Ctrl+X")
        self.edit_menu.add_command(label="Copy", command=self.copy_text, accelerator="Ctrl+C")
        self.edit_menu.add_command(label="Paste", command=self.paste_text, accelerator="Ctrl+V")
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)

        self.audio_menu = tk.Menu(self.menu_bar, tearoff=0)                                      #AUDIO FUNCTIONS
        self.audio_menu.add_command(label="Audio Settings", command=self.show_audio_settings)
        self.audio_menu.add_separator()
        self.audio_menu.add_command(label="Speech to Text", command=self.start_speech_to_text)
        self.audio_menu.add_command(label="Stop Listening", command=self.stop_speech_to_text, state='disabled')
        self.audio_menu.add_command(label="Read Aloud", command=self.text_to_speech)
        self.audio_menu.add_command(label="Stop Reading", command=self.stop_text_to_speech)
        self.menu_bar.add_cascade(label="Audio", menu=self.audio_menu)

        self.help_menu = tk.Menu(self.menu_bar, tearoff=0)                                         #HELP SUPPORT
        self.help_menu.add_command(label="About", command=self.show_about)
        self.menu_bar.add_cascade(label="Help", menu=self.help_menu)
        
        self.root.config(menu=self.menu_bar)

        self.text_area = ctk.CTkTextbox(
            self.left_frame,
            wrap=tk.WORD,
            font=("Consolas", 12),
            fg_color=("#FFFFFF", "#2B2B2B"),
            text_color=("#000000", "#FFFFFF"),
            border_width=1,
            border_color=("#CCCCCC", "#444444")
        )
        self.text_area.pack(expand=True, fill="both", padx=5, pady=5)
        
        self.audio_controls_frame = ctk.CTkFrame(self.root)
        self.audio_controls_frame.pack(fill="x", padx=5, pady=5)
        
        self.speech_to_text_btn = ctk.CTkButton(
            self.audio_controls_frame,                                           # Speech to Text button
            text="🎤 Start Dictation",
            command=self.start_speech_to_text,
            fg_color="#4CAF50",
            hover_color="#45a049"
        )
        self.speech_to_text_btn.pack(side="left", padx=5)
        
        self.stop_listening_btn = ctk.CTkButton(                                            # Stop Listening button
            self.audio_controls_frame,
            text="⏹ Stop Listening",
            command=self.stop_speech_to_text,
            fg_color="#f44336",
            hover_color="#d32f2f",
            state="disabled"
        )
        self.stop_listening_btn.pack(side="left", padx=5)
        
        self.read_aloud_btn = ctk.CTkButton(                                                   # Read Aloud button
            self.audio_controls_frame,
            text="🔊 Read Aloud",
            command=self.text_to_speech,
            fg_color="#2196F3",
            hover_color="#0b7dda"
        )
        self.read_aloud_btn.pack(side="left", padx=5)
        
        self.stop_reading_btn = ctk.CTkButton(                                             # Stop Reading button
            self.audio_controls_frame,
            text="⏹ Stop Reading",
            command=self.stop_text_to_speech,
            fg_color="#f44336",
            hover_color="#d32f2f"
        )
        self.stop_reading_btn.pack(side="left", padx=5)
        
        self.status_bar = ctk.CTkLabel(
            self.root,                                                                         # Status bar
            text="Ready",
            anchor="w",
            height=20,
            fg_color=("#F0F0F0", "#333333"),
            text_color=("#000000", "#FFFFFF")
        )
        self.status_bar.pack(fill="x", side="bottom")

        self.root.bind("<Control-n>", lambda event: self.new_file())
        self.root.bind("<Control-o>", lambda event: self.open_file())
        self.root.bind("<Control-s>", lambda event: self.save_file())
    
    def new_file(self):
        self.text_area.delete("1.0", tk.END)
        self.current_file = None
        self.update_status("New file created")
        
    def open_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, "r") as file:
                    content = file.read()
                    self.text_area.delete("1.0", tk.END)
                    self.text_area.insert("1.0", content)
                    self.current_file = file_path
                    self.update_status(f"Opened: {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open file:\n{str(e)}")
    
    def save_file(self):
        if self.current_file:
            try:
                with open(self.current_file, "w") as file:
                    content = self.text_area.get("1.0", tk.END)
                    file.write(content)
                    self.update_status(f"Saved: {self.current_file}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file:\n{str(e)}")
        else:
            self.save_file_as()
    
    def save_file_as(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, "w") as file:
                    content = self.text_area.get("1.0", tk.END)
                    file.write(content)
                    self.current_file = file_path
                    self.update_status(f"Saved: {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file:\n{str(e)}")
    
    def cut_text(self):
        self.text_area.event_generate("<<Cut>>")
        self.update_status("Text cut to clipboard")
    def copy_text(self):
        self.text_area.event_generate("<<Copy>>")
        self.update_status("Text copied to clipboard")
    def paste_text(self):
        self.text_area.event_generate("<<Paste>>")
        self.update_status("Text pasted from clipboard")
    def start_speech_to_text(self):
        if self.is_listening:
            return
            
        self.is_listening = True
        self.speech_to_text_btn.configure(state="disabled")
        self.stop_listening_btn.configure(state="normal")
        self.audio_menu.entryconfig("Stop Listening", state="normal")
        self.audio_menu.entryconfig("Speech to Text", state="disabled")
        
        self.create_3d_visualization()
        self.update_status("Listening... Speak now")

        threading.Thread(target=self._listen_to_speech, daemon=True).start()
    
    def _listen_to_speech(self):
        with sr.Microphone(device_index=self.audio_settings['stt_device_index']) as source:
            self.recognizer.energy_threshold = self.audio_settings['stt_energy_threshold']
            self.recognizer.adjust_for_ambient_noise(source)
            while self.is_listening:
                try:
                    audio = self.recognizer.listen(source, timeout=3, phrase_time_limit=5)
                    text = self.recognizer.recognize_google(audio)
                    self.text_area.insert(tk.END, text + " ")
                    self.update_status(f"Recognized: {text}")
                except sr.WaitTimeoutError:
                    continue
                except sr.UnknownValueError:
                    self.update_status("Could not understand audio")
                except Exception as e:
                    self.update_status(f"Error: {str(e)}")
                    break
    
    def stop_speech_to_text(self):
        self.is_listening = False
        self.speech_to_text_btn.configure(state="normal")
        self.stop_listening_btn.configure(state="disabled")
        self.audio_menu.entryconfig("Stop Listening", state="disabled")
        self.audio_menu.entryconfig("Speech to Text", state="normal")
        self.remove_3d_visualization()
        self.update_status("Stopped listening")
    def text_to_speech(self):
        text = self.text_area.get("1.0", tk.END).strip()
        if not text:
            self.update_status("No text to read")
            return
            
        self.create_3d_visualization()
        self.update_status("Reading text...")

        self.engine.setProperty('volume', self.audio_settings['tts_volume'])
        self.engine.setProperty('rate', self.audio_settings['tts_rate'])
        if self.tts_voices:
            self.engine.setProperty('voice', self.engine.getProperty('voices')[self.audio_settings['tts_voice']].id)
        
        threading.Thread(target=self._speak_text, args=(text,), daemon=True).start()                  #SEPERATING THREAD
    
    def _speak_text(self, text):
        self.engine.say(text)
        try:
            self.engine.runAndWait()
            self.update_status("Finished reading")
        except Exception as e:
            self.update_status(f"Error in reading: {str(e)}") 
    def stop_text_to_speech(self):
        self.engine.stop()
        self.remove_3d_visualization()
        self.update_status("Stopped reading")
    def show_audio_settings(self):
        settings_window = ctk.CTkToplevel(self.root)
        settings_window.title("Audio Settings")
        settings_window.geometry("500x400")
        settings_window.transient(self.root)
        settings_window.grab_set()
        
        # Settings Frame
        tts_frame = ctk.CTkFrame(settings_window)
        tts_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(tts_frame, text="Text-to-Speech Settings", font=("Arial", 14, "bold")).pack(pady=5)
        
        # Volume
        ctk.CTkLabel(tts_frame, text="Volume:").pack(anchor="w")
        self.volume_slider = ctk.CTkSlider(
            tts_frame,
            from_=0,
            to=1,
            number_of_steps=10,
            command=lambda v: self.update_tts_volume(v)
        )
        self.volume_slider.set(self.audio_settings['tts_volume'])
        self.volume_slider.pack(fill="x", padx=5, pady=5)
        ctk.CTkLabel(tts_frame, text="Speech Rate:").pack(anchor="w")
        self.rate_slider = ctk.CTkSlider(
            tts_frame,
            from_=100,
            to=300,
            number_of_steps=20,
            command=lambda r: self.update_tts_rate(r)
        )
        self.rate_slider.set(self.audio_settings['tts_rate'])
        self.rate_slider.pack(fill="x", padx=5, pady=5)
        
        # Voice Selection
        ctk.CTkLabel(tts_frame, text="Voice:").pack(anchor="w")
        self.voice_combobox = ttk.Combobox(
            tts_frame,
            values=[voice[1] for voice in self.tts_voices],
            state="readonly"
        )
        self.voice_combobox.current(self.audio_settings['tts_voice'])
        self.voice_combobox.pack(fill="x", padx=5, pady=5)
        self.voice_combobox.bind("<<ComboboxSelected>>", self.update_tts_voice)
        
        #Settings Frame
        stt_frame = ctk.CTkFrame(settings_window)
        stt_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(stt_frame, text="Speech-to-Text Settings", font=("Arial", 14, "bold")).pack(pady=5)
        
        ctk.CTkLabel(stt_frame, text="Microphone Sensitivity:").pack(anchor="w")
        self.sensitivity_slider = ctk.CTkSlider(
            stt_frame,
            from_=50,                                                              #MOST HEADACHE THING ARE HERE
            to=1000,
            number_of_steps=20,
            command=lambda e: self.update_stt_sensitivity(e)
        )
        self.sensitivity_slider.set(self.audio_settings['stt_energy_threshold'])
        self.sensitivity_slider.pack(fill="x", padx=5, pady=5)
        
        # INP Device Selection
        ctk.CTkLabel(stt_frame, text="Input Device:").pack(anchor="w")
        self.input_device_combobox = ttk.Combobox(
            stt_frame,
            values=[device[1] for device in self.input_devices],
            state="readonly"
        )
        if self.audio_settings['stt_device_index'] is not None:
            for i, (idx, name) in enumerate(self.input_devices):
                if idx == self.audio_settings['stt_device_index']:
                    self.input_device_combobox.current(i)
                    break
        self.input_device_combobox.pack(fill="x", padx=5, pady=5)
        self.input_device_combobox.bind("<<ComboboxSelected>>", self.update_stt_device)
        
        # Close button
        close_btn = ctk.CTkButton(
            settings_window,
            text="Close",
            command=settings_window.destroy
        )
        close_btn.pack(pady=10)
    
    def update_tts_volume(self, volume):
        self.audio_settings['tts_volume'] = volume
        self.engine.setProperty('volume', volume)
    def update_tts_rate(self, rate):
        self.audio_settings['tts_rate'] = rate
        self.engine.setProperty('rate', rate)
    def update_tts_voice(self, event):
        selected = self.voice_combobox.current()
        self.audio_settings['tts_voice'] = selected
        self.engine.setProperty('voice', self.engine.getProperty('voices')[selected].id)
    def update_stt_sensitivity(self, threshold):
        self.audio_settings['stt_energy_threshold'] = threshold
        self.recognizer.energy_threshold = threshold
    def update_stt_device(self, event):
        selected = self.input_device_combobox.current()
        if selected >= 0:
            self.audio_settings['stt_device_index'] = self.input_devices[selected][0]
    def exit_app(self):
        if messagebox.askokcancel("Exit", "Do you want to exit?"):
            self.stop_speech_to_text()
            self.stop_text_to_speech()
            self.root.destroy()
    def show_about(self):
        messagebox.showinfo(
            "About Enhanced Notepad",
            "Enhanced Notepad with Speech Features\n"
            "Includes Speech-to-Text and Text-to-Speech\n"
            "Built with Tkinter, CustomTkinter, pyttsx3, and SpeechRecognition\n"
            "Version 2.0"
        )
    
    def update_status(self, message):
        self.status_bar.configure(text=message)

if __name__ == "__main__":
    root = ctk.CTk()
    app = NotepadApp(root)
    root.mainloop()
    
    
    
    #END OF ENHANCED NOTEPAD