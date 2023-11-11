#sheets.py
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import os

class SpreadsheetApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Py-OS Sheets")

        self.menu_bar = tk.Menu(root)
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="New", command=self.new_file)
        self.file_menu.add_command(label="Open", command=self.open_file)
        self.file_menu.add_command(label="Save", command=self.save_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=root.quit)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.root.config(menu=self.menu_bar)

        self.grid = []
        self.images = {}
        self.create_grid()

    def create_grid(self):
        for row in range(10):
            row_data = []
            for col in range(10):
                cell = tk.Entry(self.root, width=10)
                cell.grid(row=row + 1, column=col + 1)
                row_data.append(cell)
            self.grid.append(row_data)

    def new_file(self):
        for row in self.grid:
            for cell in row:
                cell.delete(0, tk.END)
                cell.image = None
        self.images = {}

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Pysso Files", "*.pysso")])
        if file_path:
            self.load_from_pysso(file_path)

    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".pysso", filetypes=[("Pysso Files", "*.pysso")])
        if file_path:
            self.save_to_pysso(file_path)

    def calculate_formulas(self):
        for i, row in enumerate(self.grid):
            for j, cell in enumerate(row):
                content = cell.get()
                if content.startswith("="):
                    formula = content[1:]
                    result = self.evaluate_formula(formula)
                    cell.delete(0, tk.END)
                    cell.insert(0, result)

    def evaluate_formula(self, formula):
        try:
            formula = formula.replace("=", "")
            for i in range(10):
                for j in range(10):
                    cell_ref = self.grid[i][j].get()
                    col_letter = chr(ord("A") + j)
                    formula = formula.replace(f"{col_letter}{i + 1}", cell_ref)
            return eval(formula)
        except Exception as e:
            return f"Error: {e}"

    def choose_image(self):
        image_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.jpeg *.png *.gif")])
        if image_path:
            self.insert_image(0, 0, image_path)
    def insert_image(self, row, col, image_path):
        if os.path.exists(image_path):
            img = Image.open(image_path)
            img.thumbnail((60, 60))
            img_tk = ImageTk.PhotoImage(img)

            label = tk.Label(self.root, image=img_tk)
            label.image = img_tk
            label.grid(row=row + 1, column=col + 1)
            self.images[(row, col)] = image_path

    def save_to_pysso(self, file_path):
        with open(file_path, "w") as file:
            for i, row in enumerate(self.grid):
                row_values = []
                for j, cell in enumerate(row):
                    if (i, j) in self.images:
                        img_path = self.images[(i, j)]
                        row_values.append(f"IMG:{img_path}")
                    else:
                        row_values.append(cell.get())
                line = ",".join(row_values) + "\n"
                file.write(line)

    def load_from_pysso(self, file_path):
        if os.path.exists(file_path):
            self.new_file()
            with open(file_path, "r") as file:
                lines = file.readlines()
                for i, line in enumerate(lines):
                    values = line.strip().split(",")
                    for j, value in enumerate(values):
                        if value.startswith("IMG:"):
                            image_path = value.replace("IMG:", "")
                            self.insert_image(i, j, image_path)
                        else:
                            self.grid[i][j].delete(0, tk.END)
                            self.grid[i][j].insert(0, value)

def main():
    root = tk.Tk()
    app = SpreadsheetApp(root)

    for i in range(10):
        row_label = tk.Label(root, text=str(i + 1))
        row_label.grid(row=i + 1, column=0)

    for i in range(10):
        col_label = tk.Label(root, text=chr(ord("A") + i))
        col_label.grid(row=0, column=i + 1)

    formula_button = tk.Button(root, text="Calculate Formulas", command=app.calculate_formulas)
    formula_button.grid(row=0, column=11)

    insert_image_button = tk.Button(root, text="Insert Image", command=app.choose_image)
    insert_image_button.grid(row=0, column=12)

    root.mainloop()
if __name__ == "__main__":
    main()