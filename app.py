import customtkinter as ctk
from gui.main_gui import MainGUI
from audio.voice_module import VoiceModule
from audio.visualization import Visualization
from utils.file_operations import FileOperations
from utils.text_operations import TextOperations

class NotepadApp:
    def __init__(self, root):
        self.root = root
        self.gui = MainGUI(root)
        self.voice_module = VoiceModule(self.gui)
        self.visualization = Visualization(self.gui.right_frame)
        self.file_ops = FileOperations(self.gui)
        self.gui.set_file_operations(self.file_ops)
        self.text_ops = TextOperations(self.gui)

if __name__ == "__main__":
    root = ctk.CTk()
    app = NotepadApp(root)
    root.mainloop()