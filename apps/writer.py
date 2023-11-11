#writer.py
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import PyPDF2
import tkinter.colorchooser as colorchooser
from PIL import Image, ImageTk
import io
import base64
import re
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

class OfficeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Py-OS Writer")

        self.menu_bar = tk.Menu(root)
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="Open PDF", command=self.open_pdf)
        self.file_menu.add_command(label="Open Pysof File", command=self.open_custom_file)
        self.file_menu.add_command(label="Save File as Pysof", command=self.save_custom_file)
        self.file_menu.add_command(label="Save as PDF", command=self.save_as_pdf)  # Add the new "Save as PDF" option
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=root.quit)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.root.config(menu=self.menu_bar)

        self.create_widgets()

        self.font_sizes = [8, 10, 12, 14, 16, 18, 20]
        self.font_families = ["Arial", "Helvetica", "Times", "Courier", "Verdana", "Georgia", "Palatino"]

    def create_widgets(self):
        self.text_widget = tk.Text(self.root, wrap=tk.WORD, font=("Helvetica", 12))
        self.text_widget.pack(fill=tk.BOTH, expand=True)

        self.toolbar = tk.Frame(self.root)
        self.toolbar.pack(fill=tk.X)

        self.color_button = tk.Button(self.toolbar, text="Change Color", command=self.change_color)
        self.color_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.font_button = tk.Button(self.toolbar, text="Change Font", command=self.change_font)
        self.font_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.font_size_button = tk.Button(self.toolbar, text="Change Font Size", command=self.change_font_size)
        self.font_size_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.image_button = tk.Button(self.toolbar, text="Insert Image", command=self.insert_image)
        self.image_button.pack(side=tk.LEFT, padx=5, pady=5)

    def open_pdf(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if file_path:
            pdf_content = self.read_pdf(file_path)
            self.text_widget.delete(1.0, tk.END)
            self.text_widget.insert(tk.END, pdf_content)

    def save_as_pdf(self):
        content = self.text_widget.get("1.0", tk.END)
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
        if file_path:
            self.export_as_pdf(content, file_path)

    def export_as_pdf(self, content, file_path):
        c = canvas.Canvas(file_path, pagesize=letter)
        width, height = letter
        c.drawString(100, height - 100, content)
        c.save()
    def open_custom_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Custom Files", "*.pysof")])
        if file_path:
            custom_content = self.read_custom_file(file_path)
            self.text_widget.delete(1.0, tk.END)
            self.text_widget.insert(tk.END, custom_content)

    def save_custom_file(self):
        content = self.text_widget.get("1.0", tk.END)
        file_path = filedialog.asksaveasfilename(defaultextension=".pysof", filetypes=[("Custom Files", "*.pysof")])
        if file_path:
            with open(file_path, "w") as custom_file:
                custom_file.write(content)

    def change_color(self):
        chosen_color = colorchooser.askcolor()[1]
        self.text_widget.tag_configure("colored", foreground=chosen_color)
        selected_text = self.text_widget.tag_ranges(tk.SEL)
        if selected_text:
            self.text_widget.tag_add("colored", selected_text[0], selected_text[1])

    def change_font(self):
        chosen_font = simpledialog.askstring("Font Family", "Enter a font family:", initialvalue="Arial")
        if chosen_font and chosen_font in self.font_families:
            self.text_widget.configure(font=(chosen_font, 12))
        else:
            messagebox.showerror("Invalid Font Family", "The selected font family is not valid.")

    def change_font_size(self):
        chosen_size = self.font_sizes[simpledialog.askinteger("Font Size", "Select a font size:", minvalue=1, maxvalue=len(self.font_sizes))]
        current_font = self.text_widget.cget("font")
        font_family = current_font[0]
        self.text_widget.configure(font=(font_family, chosen_size))

    def insert_image(self):
        image_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg *.gif *.bmp")])
        if image_path:
            image = Image.open(image_path)
            photo = ImageTk.PhotoImage(image)
            self.text_widget.image_create(tk.END, image=photo)
            self.text_widget.image = photo

    def read_pdf(self, file_path):
        with open(file_path, "rb") as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text

    def read_custom_file(self, file_path):
        with open(file_path, "r") as custom_file:
            content = custom_file.read()

        image_starts = [match.start() for match in re.finditer(r'\[IMAGE\]', content)]
        image_ends = [match.end() for match in re.finditer(r'\[/IMAGE\]', content)]

        image_ranges = list(zip(image_starts, image_ends))

        content_without_images = re.sub(r'\[IMAGE\].*?\[/IMAGE\]', '', content)
        self.text_widget.delete(1.0, tk.END)
        self.text_widget.insert(tk.END, content_without_images)

        for start, end in image_ranges:
            image_data = content[start + 7:end - 8]
            if image_data:
                image_data = image_data.encode("utf-8")
                image = Image.open(io.BytesIO(base64.b64decode(image_data)))
                photo = ImageTk.PhotoImage(image)
                self.text_widget.image_create(tk.END, image=photo)
                self.text_widget.image = photo

        return content_without_images

def main():
    root = tk.Tk()
    app = OfficeApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
