import tkinter as tk
from tkinter import ttk, filedialog, messagebox

class TextEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Text Editor")

        style = ttk.Style()
        style.theme_use("clam")

        frame = ttk.Frame(root)
        frame.pack(expand="yes", fill="both", padx=5, pady=5)

        text_scrollbar = tk.Scrollbar(frame, orient="vertical")
        text_scrollbar.pack(side="right", fill="y")

        self.row_numbers_widget = tk.Text(frame, width=3, bg='white', fg='black', padx=5, pady=5, font=('Arial', 12), wrap="none")
        self.row_numbers_widget.pack(side="left", fill="y")

        self.main_text_widget = tk.Text(frame, wrap='word', undo=True, bg='white', fg='black', insertbackground='black', padx=5, pady=5, font=('Arial', 12), yscrollcommand=text_scrollbar.set)
        self.main_text_widget.pack(expand="yes", fill="both", padx=(0, 5))

        text_scrollbar.config(command=self.main_text_widget.yview)

        self.main_text_widget.config(yscrollcommand=self.scroll_text)
        self.row_numbers_widget.config(state='disabled', bg='white', fg='black', font=('Arial', 12))

        self.menu_bar = tk.Menu(root)
        self.root.config(menu=self.menu_bar)

        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="New", command=self.new_file)
        self.file_menu.add_command(label="Open", command=self.open_file)
        self.file_menu.add_command(label="Save", command=self.save_file)
        self.file_menu.add_command(label="Save As", command=self.save_file_as)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=root.destroy)

        self.edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)
        self.edit_menu.add_command(label="Cut", command=self.cut_text)
        self.edit_menu.add_command(label="Copy", command=self.copy_text)
        self.edit_menu.add_command(label="Paste", command=self.paste_text)
        self.edit_menu.add_command(label="Undo", command=self.main_text_widget.edit_undo, accelerator="Ctrl+Z")
        self.edit_menu.add_command(label="Redo", command=self.main_text_widget.edit_redo, accelerator="Ctrl+Y")

        self.about_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="About", menu=self.about_menu)
        self.about_menu.add_command(label="About", command=self.show_about_info)

        self.main_text_widget.bind('<Configure>', self.on_text_configure)
        self.main_text_widget.bind('<Key>', self.on_text_key)

        self.update_row_numbers()

        root.bind("<Control-n>", lambda: self.new_file())
        root.bind("<Control-o>", lambda: self.open_file())
        root.bind("<Control-s>", lambda: self.save_file())
        root.bind("<Control-S>", lambda: self.save_file_as())
        root.bind("<Control-x>", lambda: self.cut_text())
        root.bind("<Control-c>", lambda: self.copy_text())
        root.bind("<Control-v>", lambda: self.paste_text())
        root.bind("<Control-z>", lambda: self.main_text_widget.edit_undo())
        root.bind("<Control-y>", lambda: self.main_text_widget.edit_redo())

        self.format_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Format", menu=self.format_menu)
        self.format_menu.add_command(label="Bold", command=self.toggle_bold, accelerator="Ctrl+B")
        self.format_menu.add_command(label="Italic", command=self.toggle_italic, accelerator="Ctrl+I")
        self.format_menu.add_command(label="Underline", command=self.toggle_underline, accelerator="Ctrl+U")
        self.format_menu.add_separator()
        self.font_menu = tk.Menu(self.format_menu, tearoff=0)
        self.format_menu.add_cascade(label="Font", menu=self.font_menu)
        self.font_var = tk.StringVar()
        self.font_menu.add_radiobutton(label="Arial", variable=self.font_var, value="Arial", command=self.change_font)
        self.font_menu.add_radiobutton(label="Courier New", variable=self.font_var, value="Courier New", command=self.change_font)
        self.font_menu.add_radiobutton(label="Times New Roman", variable=self.font_var, value="Times New Roman", command=self.change_font)

        self.bold_var = tk.BooleanVar()
        self.italic_var = tk.BooleanVar()
        self.underline_var = tk.BooleanVar()

        self.main_text_widget.tag_configure("bold", font=('Arial', 12, 'bold'))
        self.main_text_widget.tag_configure("italic", font=('Arial', 12, 'italic'))
        self.main_text_widget.tag_configure("underline", underline=True)

        self.context_menu = tk.Menu(root, tearoff=0)
        self.context_menu.add_command(label="Cut", command=self.cut_text)
        self.context_menu.add_command(label="Copy", command=self.copy_text)
        self.context_menu.add_command(label="Paste", command=self.paste_text)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Bold", command=self.toggle_bold)
        self.context_menu.add_command(label="Italic", command=self.toggle_italic)
        self.context_menu.add_command(label="Underline", command=self.toggle_underline)

        self.main_text_widget.bind("<Button-3>", self.show_context_menu)

    def show_context_menu(self, event):
        self.context_menu.post(event.x_root, event.y_root)

    def on_text_configure(self, event):
        self.update_row_numbers()

    def on_text_key(self, event):
        self.update_row_numbers()

    def scroll_text(self, *args):
        self.row_numbers_widget.yview_moveto(args[0])
        self.main_text_widget.yview_moveto(args[0])

    def update_row_numbers(self):
        lines = self.main_text_widget.get(1.0, tk.END).count('\n')
        row_numbers_text = '\n'.join(str(i) for i in range(1, lines + 2))
        self.row_numbers_widget.config(state='normal')
        self.row_numbers_widget.delete(1.0, tk.END)
        self.row_numbers_widget.insert(tk.END, row_numbers_text)
        self.row_numbers_widget.config(state='disabled')

    def new_file(self):
        self.main_text_widget.delete(1.0, tk.END)
        self.update_row_numbers()

    def open_file(self):
        file_path = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("Html files", "*.html"), ("Python files", "*.py"), ("All files", "*.*")])
        if file_path:
            with open(file_path, "r") as file:
                content = file.read()
                self.main_text_widget.delete(1.0, tk.END)
                self.main_text_widget.insert(tk.END, content)
                self.update_row_numbers()

    def save_file(self):
        if not hasattr(self, "file_path"):
            self.save_file_as()
        else:
            content = self.main_text_widget.get(1.0, tk.END)
            with open(self.file_path, "w") as file:
                file.write(content)

    def save_file_as(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("Html files", "*.html"), ("Python files", "*.py"), ("All files", "*.*")])
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
        tk.messagebox.showinfo("About", "Joel Editor\n\nCreated by Veol Steve")

    def toggle_bold(self):
        self.toggle_formatting("bold", self.bold_var)

    def toggle_italic(self):
        self.toggle_formatting("italic", self.italic_var)

    def toggle_underline(self):
        self.toggle_formatting("underline", self.underline_var)

    def toggle_formatting(self, tag, variable):
        current_tags = self.main_text_widget.tag_names(tk.SEL_FIRST)
        if tag in current_tags:
            self.main_text_widget.tag_remove(tag, tk.SEL_FIRST, tk.SEL_LAST)
            variable.set(False)
        else:
            self.main_text_widget.tag_add(tag, tk.SEL_FIRST, tk.SEL_LAST)
            variable.set(True)

    def change_font(self):
        font_name = self.font_var.get()
        self.main_text_widget.configure(font=(font_name, 12))


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x600")
    editor = TextEditor(root)
    root.mainloop()
