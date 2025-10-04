import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, font
import os

class Notepad:
    def __init__(self, root):
        self.root = root
        self.root.title("Untitled - Notepad")
        self.root.geometry("900x650")
        self.filepath = None
        self.default_font = font.Font(family="Helvetica", size=12)
        self._create_menu()
        self._create_toolbar()
        self._create_text_area()
        self._create_status_bar()
        self._bind_shortcuts()
        self._update_status()

    def _create_menu(self):
        menubar = tk.Menu(self.root)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="New", accelerator="Ctrl+N", command=self.new_file)
        file_menu.add_command(label="Open...", accelerator="Ctrl+O", command=self.open_file)
        file_menu.add_command(label="Save", accelerator="Ctrl+S", command=self.save_file)
        file_menu.add_command(label="Save As...", accelerator="Ctrl+Shift+S", command=self.save_as)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", accelerator="Ctrl+Q", command=self.exit_app)
        menubar.add_cascade(label="File", menu=file_menu)

        edit_menu = tk.Menu(menubar, tearoff=0)
        edit_menu.add_command(label="Undo", accelerator="Ctrl+Z", command=lambda: self.text_event.event_generate("<<Undo>>"))
        edit_menu.add_command(label="Redo", accelerator="Ctrl+Y", command=lambda: self.text_event.event_generate("<<Redo>>"))
        edit_menu.add_separator()
        edit_menu.add_command(label="Cut", accelerator="Ctrl+X", command=lambda: self.text_event.event_generate("<<Cut>>"))
        edit_menu.add_command(label="Copy", accelerator="Ctrl+C", command=lambda: self.text_event.event_generate("<<Copy>>"))
        edit_menu.add_command(label="Paste", accelerator="Ctrl+V", command=lambda: self.text_event.event_generate("<<Paste>>"))
        edit_menu.add_separator()
        edit_menu.add_command(label="Find", accelerator="Ctrl+F", command=self.find_text)
        edit_menu.add_command(label="Replace", accelerator="Ctrl+H", command=self.replace_text)
        edit_menu.add_separator()
        edit_menu.add_command(label="Select All", accelerator="Ctrl+A", command=lambda: self.text_event.tag_add('sel', '1.0', 'end'))
        edit_menu.add_command(label="Clear", command=lambda: self.text_event.delete('1.0', 'end'))
        menubar.add_cascade(label="Edit", menu=edit_menu)

        view_menu = tk.Menu(menubar, tearoff=0)
        view_menu.add_command(label="Increase Font", command=lambda: self._change_font_size(2))
        view_menu.add_command(label="Decrease Font", command=lambda: self._change_font_size(-2))
        menubar.add_cascade(label="View", menu=view_menu)

        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="About", command=self._about)
        menubar.add_cascade(label="Help", menu=help_menu)
        self.root.config(menu=menubar)

    def _create_toolbar(self):
        toolbar = tk.Frame(self.root, bd=1, relief=tk.RAISED)
        toolbar.pack(side=tk.TOP, fill=tk.X)
        new_btn = tk.Button(toolbar, text="New", command=self.new_file)
        new_btn.pack(side=tk.LEFT, padx=2, pady=2)
        open_btn = tk.Button(toolbar, text="Open", command=self.open_file)
        open_btn.pack(side=tk.LEFT, padx=2, pady=2)
        save_btn = tk.Button(toolbar, text="Save", command=self.save_file)
        save_btn.pack(side=tk.LEFT, padx=2, pady=2)
        tk.Label(toolbar, text=" ").pack(side=tk.LEFT)
        find_btn = tk.Button(toolbar, text="Find", command=self.find_text)
        find_btn.pack(side=tk.LEFT, padx=2, pady=2)
        replace_btn = tk.Button(toolbar, text="Replace", command=self.replace_text)
        replace_btn.pack(side=tk.LEFT, padx=2, pady=2)

    def _create_text_area(self):
        text_frame = tk.Frame(self.root)
        text_frame.pack(fill=tk.BOTH, expand=1)
        self.linenumbers = tk.Text(text_frame, width=4, padx=4, takefocus=0, border=0, background="#f0f0f0", state='disabled')
        self.linenumbers.pack(side=tk.LEFT, fill=tk.Y)
        self.text_event = tk.Text(text_frame, wrap='word', undo=True)
        self.text_event.configure(font=self.default_font)
        self.text_event.pack(fill=tk.BOTH, expand=1, side=tk.LEFT)
        scroll = tk.Scrollbar(text_frame, command=self._on_scroll)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_event.config(yscrollcommand=scroll.set)
        self.text_event.bind('<KeyRelease>', lambda e: self._update_line_numbers())
        self.text_event.bind('<ButtonRelease>', lambda e: self._update_line_numbers())

    def _create_status_bar(self):
        self.status = tk.StringVar()
        self.status.set('Ln 1, Col 0')
        status_bar = tk.Label(self.root, textvariable=self.status, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def new_file(self, event=None):
        if self._maybe_save():
            self.text_event.delete('1.0', tk.END)
            self.filepath = None
            self.root.title('Untitled - Notepad')
            self._update_line_numbers()

    def open_file(self, event=None):
        if not self._maybe_save():
            return
        path = filedialog.askopenfilename(filetypes=[('Text Files', '*.txt'), ('All Files', '*.*')])
        if path:
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    data = f.read()
                self.text_event.delete('1.0', tk.END)
                self.text_event.insert('1.0', data)
                self.filepath = path
                self.root.title(f"{os.path.basename(path)} - Notepad")
                self._update_line_numbers()
            except Exception as e:
                messagebox.showerror('Error', f'Could not open file: {e}')

    def save_file(self, event=None):
        if self.filepath:
            try:
                with open(self.filepath, 'w', encoding='utf-8') as f:
                    f.write(self.text_event.get('1.0', tk.END))
                messagebox.showinfo('Saved', 'File saved successfully')
            except Exception as e:
                messagebox.showerror('Error', f'Could not save file: {e}')
        else:
            self.save_as()

    def save_as(self, event=None):
        path = filedialog.asksaveasfilename(defaultextension='.txt', filetypes=[('Text Files', '*.txt'), ('All Files', '*.*')])
        if path:
            try:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(self.text_event.get('1.0', tk.END))
                self.filepath = path
                self.root.title(f"{os.path.basename(path)} - Notepad")
                messagebox.showinfo('Saved', 'File saved successfully')
            except Exception as e:
                messagebox.showerror('Error', f'Could not save file: {e}')

    def exit_app(self, event=None):
        if self._maybe_save():
            self.root.quit()

    def _maybe_save(self):
        if self.text_event.edit_modified():
            res = messagebox.askyesnocancel('Save', 'Do you want to save changes?')
            if res:
                self.save_file()
                return True
            elif res is False:
                return True
            else:
                return False
        return True

    def find_text(self, event=None):
        s = simpledialog.askstring('Find', 'Enter text to find:')
        if s:
            start = '1.0'
            self.text_event.tag_remove('found', '1.0', tk.END)
            count = tk.IntVar()
            while True:
                pos = self.text_event.search(s, start, stopindex=tk.END, count=count)
                if not pos:
                    break
                end = f"{pos}+{count.get()}c"
                self.text_event.tag_add('found', pos, end)
                start = end
            self.text_event.tag_config('found', background='yellow')

    def replace_text(self, event=None):
        find = simpledialog.askstring('Replace', 'Find:')
        if find is None:
            return
        replace = simpledialog.askstring('Replace', 'Replace with:')
        if replace is None:
            return
        data = self.text_event.get('1.0', tk.END)
        new = data.replace(find, replace)
        self.text_event.delete('1.0', tk.END)
        self.text_event.insert('1.0', new)

    def _on_scroll(self, *args):
        self.text_event.yview(*args)
        self.linenumbers.yview(*args)

    def _update_line_numbers(self):
        self.linenumbers.configure(state='normal')
        self.linenumbers.delete('1.0', tk.END)
        line_count = int(self.text_event.index('end-1c').split('.')[0])
        nums = '\n'.join(str(i) for i in range(1, line_count+1))
        self.linenumbers.insert('1.0', nums + '\n')
        self.linenumbers.configure(state='disabled')

    def _update_status(self):
        index = self.text_event.index(tk.INSERT)
        line, col = index.split('.')
        self.status.set(f'Ln {line}, Col {col}')
        self.root.after(200, self._update_status)

    def _change_font_size(self, delta):
        size = self.default_font['size'] + delta
        if size < 8:
            size = 8
        self.default_font.configure(size=size)

    def _bind_shortcuts(self):
        self.root.bind('<Control-n>', self.new_file)
        self.root.bind('<Control-o>', self.open_file)
        self.root.bind('<Control-s>', self.save_file)
        self.root.bind('<Control-S>', self.save_as)
        self.root.bind('<Control-q>', self.exit_app)
        self.root.bind('<Control-f>', self.find_text)
        self.root.bind('<Control-h>', self.replace_text)
        self.text_event.bind('<<Modified>>', self._on_modified)

    def _on_modified(self, event=None):
        self.text_event.edit_modified(True)

    def _about(self):
        messagebox.showinfo('About', 'Simple Notepad\nBuilt with Tkinter\n(You can extend it!)')

if __name__ == '__main__':
    root = tk.Tk()
    app = Notepad(root)
    root.mainloop()
