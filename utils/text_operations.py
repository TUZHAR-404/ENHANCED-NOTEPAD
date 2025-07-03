class TextOperations:
    def __init__(self, gui):
        self.gui = gui

    def cut_text(self):
        self.gui.text_area.event_generate("<<Cut>>")
        self.gui.update_status("Text cut to clipboard")

    def copy_text(self):
        self.gui.text_area.event_generate("<<Copy>>")
        self.gui.update_status("Text copied to clipboard")

    def paste_text(self):
        self.gui.text_area.event_generate("<<Paste>>")
        self.gui.update_status("Text pasted from clipboard")