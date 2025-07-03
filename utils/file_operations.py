from tkinter import filedialog, messagebox

class FileOperations:
    def __init__(self, gui):
        self.gui = gui
        self.current_file = None

    def new_file(self):
        self.gui.text_area.delete("1.0", "end")
        self.current_file = None
        self.gui.update_status("New file created")

    def open_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, "r") as file:
                    content = file.read()
                    self.gui.text_area.delete("1.0", "end")
                    self.gui.text_area.insert("1.0", content)
                    self.current_file = file_path
                    self.gui.update_status(f"Opened: {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open file:\n{str(e)}")

    def save_file(self):
        if self.current_file:
            try:
                with open(self.current_file, "w") as file:
                    content = self.gui.text_area.get("1.0", "end")
                    file.write(content)
                    self.gui.update_status(f"Saved: {self.current_file}")
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
                    content = self.gui.text_area.get("1.0", "end")
                    file.write(content)
                    self.current_file = file_path
                    self.gui.update_status(f"Saved: {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file:\n{str(e)}")