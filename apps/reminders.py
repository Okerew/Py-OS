#reminders.py
import tkinter as tk
from tkinter import messagebox

class reminders:
    def __init__(self, root):
        self.root = root
        self.root.title("Reminders")

        self.tasks = []
        self.load_tasks()

        self.task_entry = tk.Entry(root, width=40)
        self.task_entry.pack(pady=10)

        self.add_button = tk.Button(root, text="Add Task", command=self.add_task)
        self.add_button.pack(pady=5)

        self.task_listbox = tk.Listbox(root, width=40)
        self.task_listbox.pack()

        self.delete_button = tk.Button(root, text="Delete Task", command=self.delete_task)
        self.delete_button.pack(pady=5)

        self.update_task_listbox()

    def load_tasks(self):
        try:
            with open("tasks.txt", "r") as file:
                self.tasks = [line.strip() for line in file.readlines()]
        except FileNotFoundError:
            self.tasks = []

    def save_tasks(self):
        with open("tasks.txt", "w") as file:
            for task in self.tasks:
                file.write(task + "\n")

    def add_task(self):
        task = self.task_entry.get()
        if task:
            self.tasks.append(task)
            self.update_task_listbox()
            self.save_tasks()
            self.task_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Warning", "Please enter a task.")

    def update_task_listbox(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.tasks:
            self.task_listbox.insert(tk.END, task)

    def delete_task(self):
        selected_indices = self.task_listbox.curselection()
        if selected_indices:
            selected_index = selected_indices[0]
            del self.tasks[selected_index]
            self.update_task_listbox()
            self.save_tasks()
        else:
            messagebox.showwarning("Warning", "Please select a task to delete.")

def main():
    root = tk.Tk()
    app = reminders(root)
    root.mainloop()

if __name__ == "__main__":
    main()
