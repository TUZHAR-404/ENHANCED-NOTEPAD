import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk

class MainGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Audio Notepad")
        self.root.geometry("1200x800")
        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("blue")

        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(expand=True, fill="both", padx=5, pady=5)

        self.left_frame = ctk.CTkFrame(self.main_frame)
        self.left_frame.pack(side="left", expand=True, fill="both", padx=5, pady=5)

        self.right_frame = ctk.CTkFrame(self.main_frame, width=400)
        self.right_frame.pack(side="right", fill="both", padx=5, pady=5)
        self.right_frame.pack_propagate(False)

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

        self.status_bar = ctk.CTkLabel(
            self.root,
            text="Ready",
            anchor="w",
            height=20,
            fg_color=("#F0F0F0", "#333333"),
            text_color=("#000000", "#FFFFFF")
        )
        self.status_bar.pack(fill="x", side="bottom")

        self.create_menu()
        self.create_audio_controls()

        # Placeholder for file operations
        self.file_operations = None

    def set_file_operations(self, file_operations):
        """Sets the file operations instance."""
        self.file_operations = file_operations
        self.update_status("File operations initialized.")

    def create_menu(self):
        self.menu_bar = tk.Menu(self.root)

        # File menu
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="New", command=self.new_file, accelerator="Ctrl+N")
        self.file_menu.add_command(label="Open", command=self.open_file, accelerator="Ctrl+O")
        self.file_menu.add_command(label="Save", command=self.save_file, accelerator="Ctrl+S")
        self.file_menu.add_command(label="Save As", command=self.save_file_as)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.exit_app)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)

        # Edit menu
        self.edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.edit_menu.add_command(label="Cut", command=self.cut_text, accelerator="Ctrl+X")
        self.edit_menu.add_command(label="Copy", command=self.copy_text, accelerator="Ctrl+C")
        self.edit_menu.add_command(label="Paste", command=self.paste_text, accelerator="Ctrl+V")
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)

        # Audio menu
        self.audio_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.audio_menu.add_command(label="Audio Settings", command=self.show_audio_settings)
        self.audio_menu.add_separator()
        self.audio_menu.add_command(label="Speech to Text", command=self.start_speech_to_text)
        self.audio_menu.add_command(label="Stop Listening", command=self.stop_speech_to_text, state='disabled')
        self.audio_menu.add_command(label="Read Aloud", command=self.start_text_to_speech)
        self.audio_menu.add_command(label="Stop Reading", command=self.stop_text_to_speech)
        self.menu_bar.add_cascade(label="Audio", menu=self.audio_menu)

        # Help menu
        self.help_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.help_menu.add_command(label="About", command=self.show_about)
        self.menu_bar.add_cascade(label="Help", menu=self.help_menu)

        self.root.config(menu=self.menu_bar)

    def create_audio_controls(self):
        self.audio_controls_frame = ctk.CTkFrame(self.root)
        self.audio_controls_frame.pack(fill="x", padx=5, pady=5)

        self.speech_to_text_btn = ctk.CTkButton(
            self.audio_controls_frame,
            text="🎤 Start Dictation",
            command=self.start_speech_to_text,
            fg_color="#4CAF50",
            hover_color="#45a049"
        )
        self.speech_to_text_btn.pack(side="left", padx=5)

        self.stop_listening_btn = ctk.CTkButton(
            self.audio_controls_frame,
            text="⏹ Stop Listening",
            command=self.stop_speech_to_text,
            fg_color="#f44336",
            hover_color="#d32f2f",
            state="disabled"
        )
        self.stop_listening_btn.pack(side="left", padx=5)

        self.read_aloud_btn = ctk.CTkButton(
            self.audio_controls_frame,
            text="🔊 Read Aloud",
            command=self.start_text_to_speech,
            fg_color="#2196F3",
            hover_color="#0b7dda"
        )
        self.read_aloud_btn.pack(side="left", padx=5)

        self.stop_reading_btn = ctk.CTkButton(
            self.audio_controls_frame,
            text="⏹ Stop Reading",
            command=self.stop_text_to_speech,
            fg_color="#f44336",
            hover_color="#d32f2f"
        )
        self.stop_reading_btn.pack(side="left", padx=5)

    def update_status(self, message):
        self.status_bar.configure(text=message)

    def new_file(self):
        """Clears the text area for a new file."""
        self.text_area.delete("1.0", tk.END)
        self.update_status("New file created.")

    def open_file(self):
        """Opens a file and loads its content into the text area."""
        file_path = filedialog.askopenfilename(
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if file_path:
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
                self.text_area.delete("1.0", tk.END)
                self.text_area.insert("1.0", content)
            self.update_status(f"Opened file: {file_path}")

    def save_file(self):
        """Saves the current content of the text area to a file."""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if file_path:
            with open(file_path, "w", encoding="utf-8") as file:
                content = self.text_area.get("1.0", tk.END).strip()
                file.write(content)
            self.update_status(f"Saved file: {file_path}")

    def save_file_as(self):
        """Saves the current content of the text area to a new file."""
        self.save_file()

    def exit_app(self):
        """Closes the application."""
        self.root.quit()

    def cut_text(self):
        """Cuts the selected text to the clipboard."""
        self.text_area.event_generate("<<Cut>>")
        self.update_status("Text cut to clipboard.")

    def copy_text(self):
        """Copies the selected text to the clipboard."""
        self.text_area.event_generate("<<Copy>>")
        self.update_status("Text copied to clipboard.")

    def paste_text(self):
        """Pastes text from the clipboard."""
        self.text_area.event_generate("<<Paste>>")
        self.update_status("Text pasted from clipboard.")

    def show_audio_settings(self):
        """Displays the audio settings dialog."""
        messagebox.showinfo("Audio Settings", "Audio settings dialog not implemented yet.")

    def start_speech_to_text(self):
        """Starts speech-to-text functionality."""
        self.update_status("Speech-to-text started.")

    def stop_speech_to_text(self):
        """Stops speech-to-text functionality."""
        self.update_status("Speech-to-text stopped.")

    def start_text_to_speech(self):
        """Starts text-to-speech functionality."""
        self.update_status("Text-to-speech started.")

    def stop_text_to_speech(self):
        """Stops text-to-speech functionality."""
        self.update_status("Text-to-speech stopped.")

    def show_about(self):
        """Displays the About dialog."""
        messagebox.showinfo("About", "Enhanced Notepad\nVersion 1.0\nDeveloped by Collaboration Team.")