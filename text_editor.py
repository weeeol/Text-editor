import tkinter as tk
from tkinter import ttk, filedialog, messagebox

class TextEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Text Editor")
        self.file_path = None

        self.is_dark_mode = False
        self.light_bg = "white"
        self.light_fg = "black"
        self.dark_bg = "#2e2e2e"  
        self.dark_fg = "#f8f8f2"  

        style = ttk.Style()
        style.theme_use("clam")

        frame = ttk.Frame(root)
        frame.pack(expand="yes", fill="both", padx=5, pady=5)

        text_scrollbar = tk.Scrollbar(frame, orient="vertical")
        text_scrollbar.pack(side="right", fill="y")

        self.row_numbers_widget = tk.Text(frame, width=3, bg=self.light_bg, fg=self.light_fg, padx=5, pady=5, font=('Arial', 13), wrap="none")
        self.row_numbers_widget.pack(side="left", fill="y")
        self.row_numbers_widget.bind("<MouseWheel>", lambda event: "break")
        self.row_numbers_widget.bind("<Button-1>", lambda event: "break")
        self.row_numbers_widget.bind("<Key>", lambda event: "break")

        self.main_text_widget = tk.Text(frame, wrap='word', undo=True, bg=self.light_bg, fg=self.light_fg, insertbackground=self.light_fg, padx=5, pady=5, font=('Arial', 13), yscrollcommand=text_scrollbar.set)
        self.main_text_widget.pack(expand="yes", fill="both", padx=(0, 5))

        text_scrollbar.config(command=self.main_text_widget.yview)

        self.main_text_widget.config(yscrollcommand=self.scroll_text)
        self.row_numbers_widget.config(state='disabled', bg=self.light_bg, fg=self.light_fg, font=('Arial', 13))

        self.menu_bar = tk.Menu(root)
        self.root.config(menu=self.menu_bar)

        # File Menu
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="New", command=self.new_file, accelerator="Ctrl+N")
        self.file_menu.add_command(label="Open", command=self.open_file, accelerator="Ctrl+O")
        self.file_menu.add_command(label="Save", command=self.save_file, accelerator="Ctrl+S")
        self.file_menu.add_command(label="Save As", command=self.save_file_as, accelerator="Ctrl+Shift+S")
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=root.quit)

        # Edit Menu
        self.edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)
        self.edit_menu.add_command(label="Cut", command=self.cut_text, accelerator="Ctrl+X")
        self.edit_menu.add_command(label="Copy", command=self.copy_text, accelerator="Ctrl+C")
        self.edit_menu.add_command(label="Paste", command=self.paste_text, accelerator="Ctrl+V")
        self.edit_menu.add_command(label="Undo", command=self.main_text_widget.edit_undo, accelerator="Ctrl+Z")
        self.edit_menu.add_command(label="Redo", command=self.main_text_widget.edit_redo, accelerator="Ctrl+Y")

        # Format Menu
        self.format_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Format", menu=self.format_menu)
        self.format_menu.add_command(label="Bold", command=self.toggle_bold, accelerator="Ctrl+B")
        self.format_menu.add_command(label="Italic", command=self.toggle_italic, accelerator="Ctrl+I")
        self.format_menu.add_command(label="Underline", command=self.toggle_underline, accelerator="Ctrl+U")
        self.format_menu.add_separator()

        # Font Menu
        self.font_menu = tk.Menu(self.format_menu, tearoff=0)
        self.format_menu.add_cascade(label="Font", menu=self.font_menu)
        self.font_var = tk.StringVar(value="Arial")
        self.font_menu.add_radiobutton(label="Arial", variable=self.font_var, value="Arial", command=self.change_font)
        self.font_menu.add_radiobutton(label="Courier New", variable=self.font_var, value="Courier New", command=self.change_font)
        self.font_menu.add_radiobutton(label="Times New Roman", variable=self.font_var, value="Times New Roman", command=self.change_font)
        self.font_menu.add_radiobutton(label="Cascadia", variable=self.font_var, value="Cascadia", command=self.change_font)

        # Settings Menu
        self.settings_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Settings", menu=self.settings_menu)
        self.settings_menu.add_command(label="Toggle Dark Mode", command=self.toggle_dark_mode)

        # About Menu
        self.about_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="About", menu=self.about_menu)
        self.about_menu.add_command(label="About", command=self.show_about_info)

        # Configure tags for formatting
        self.main_text_widget.tag_configure("bold", font=('Arial', 12, 'bold'))
        self.main_text_widget.tag_configure("italic", font=('Arial', 12, 'italic'))
        self.main_text_widget.tag_configure("underline", underline=True)

        # Context Menu
        self.context_menu = tk.Menu(root, tearoff=0)
        self.context_menu.add_command(label="Cut", command=self.cut_text)
        self.context_menu.add_command(label="Copy", command=self.copy_text)
        self.context_menu.add_command(label="Paste", command=self.paste_text)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Bold", command=self.toggle_bold)
        self.context_menu.add_command(label="Italic", command=self.toggle_italic)
        self.context_menu.add_command(label="Underline", command=self.toggle_underline)

        self.main_text_widget.bind("<Button-3>", self.show_context_menu)

        # Event bindings
        self.main_text_widget.bind('<Configure>', self.on_text_configure)
        self.main_text_widget.bind('<Key>', self.on_text_key)

        self.update_row_numbers()
        self.update_id = None

        root.bind("<Control-n>", lambda event: self.new_file())
        root.bind("<Control-o>", lambda event: self.open_file())
        root.bind("<Control-s>", lambda event: self.save_file())
        root.bind("<Control-S>", lambda event: self.save_file_as())
        root.bind("<Control-x>", lambda event: self.cut_text())
        root.bind("<Control-c>", lambda event: self.copy_text())
        root.bind("<Control-v>", lambda event: self.paste_text())
        root.bind("<Control-z>", lambda event: self.main_text_widget.edit_undo())
        root.bind("<Control-y>", lambda event: self.main_text_widget.edit_redo())

    def toggle_dark_mode(self):
        if self.is_dark_mode:
            self.apply_light_mode()
        else:
            self.apply_dark_mode()

    def apply_light_mode(self):
        self.is_dark_mode = False
        self.main_text_widget.config(bg=self.light_bg, fg=self.light_fg, insertbackground=self.light_fg)
        self.row_numbers_widget.config(bg=self.light_bg, fg=self.light_fg)

    def apply_dark_mode(self):
        self.is_dark_mode = True
        self.main_text_widget.config(bg=self.dark_bg, fg=self.dark_fg, insertbackground=self.dark_fg)
        self.row_numbers_widget.config(bg=self.dark_bg, fg=self.dark_fg)

    def show_context_menu(self, event):
        self.context_menu.post(event.x_root, event.y_root)

    def on_text_configure(self, event):
        self.update_row_numbers()

    def on_text_key(self, event):
        if self.update_id:
            self.root.after_cancel(self.update_id)
        self.update_id = self.root.after(100, self.update_row_numbers)

    def scroll_text(self, *args):
            self.row_numbers_widget.yview_moveto(args[0])
            self.main_text_widget.yview_moveto(args[0])
            self.update_row_numbers()  

    def update_row_numbers(self):
        self.row_numbers_widget.config(state='normal')  
        self.row_numbers_widget.delete(1.0, tk.END) 
        line_count = self.main_text_widget.index('end-1c').split('.')[0]
        row_numbers = "\n".join(str(i) for i in range(1, int(line_count)+1))
        self.row_numbers_widget.insert(tk.END, row_numbers)
        self.row_numbers_widget.config(state='disabled')
        self.row_numbers_widget.yview_moveto(self.main_text_widget.yview()[0])

    def on_text_configure(self, event):
        self.update_row_numbers()

    def on_text_key(self, event):
        if self.update_id:
            self.root.after_cancel(self.update_id)
        self.update_id = self.root.after(100, self.update_row_numbers)  # Delayed update to prevent multiple triggers

    def new_file(self):
        self.main_text_widget.delete(1.0, tk.END)
        self.file_path = None
        self.root.title("Text Editor - New File")
        self.update_row_numbers()

    def open_file(self):
        file_path = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("Python files", "*.py"), ("All files", "*.*")])
        if file_path:
            try:
                with open(file_path, "r") as file:
                    content = file.read()
                    self.main_text_widget.delete(1.0, tk.END)
                    self.main_text_widget.insert(tk.END, content)
                    self.file_path = file_path
                    self.root.title(f"Text Editor - {file_path}")
                    self.update_row_numbers()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open file: {e}")

    def save_file(self):
        if not self.file_path:
            self.save_file_as()
        else:
            try:
                content = self.main_text_widget.get(1.0, tk.END)
                with open(self.file_path, "w") as file:
                    file.write(content)
                self.root.title(f"Text Editor - {self.file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {e}")

    def save_file_as(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("Python files", "*.py"), ("All files", "*.*")])
        if file_path:
            self.file_path = file_path
            self.save_file()

    def cut_text(self):
        self.main_text_widget.event_generate("<<Cut>>")
        self.update_row_numbers()

    def copy_text(self):
        self.main_text_widget.event_generate("<<Copy>>")

    def paste_text(self):
        self.main_text_widget.event_generate("<<Paste>>")
        self.update_row_numbers()

    def show_about_info(self):
        messagebox.showinfo("About", "Text Editor\n\nCreated by Veol Steve")

    def toggle_bold(self):
        self.toggle_formatting("bold")

    def toggle_italic(self):
        self.toggle_formatting("italic")

    def toggle_underline(self):
        self.toggle_formatting("underline")

    def toggle_formatting(self, tag_name):
        try:
            current_tags = self.main_text_widget.tag_names(tk.SEL_FIRST)
        except tk.TclError:
            return
        if tag_name in current_tags:
            self.main_text_widget.tag_remove(tag_name, tk.SEL_FIRST, tk.SEL_LAST)
        else:
            self.main_text_widget.tag_add(tag_name, tk.SEL_FIRST, tk.SEL_LAST)

    def change_font(self):
        selected_font = self.font_var.get()
        self.main_text_widget.config(font=(selected_font, 12))

if __name__ == "__main__":
    root = tk.Tk()
    app = TextEditor(root)
    root.geometry("800x600")
    root.mainloop()
