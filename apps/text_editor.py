# text_editor.py
import builtins
from prompt_toolkit import prompt
from prompt_toolkit.shortcuts import CompleteStyle
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.keys import Keys
from prompt_toolkit.key_binding import KeyBindings

class TextEditor:
    def __init__(self):
        self.buffer = []
        self.cursor_x = 0
        self.cursor_y = 0
        self.key_bindings = KeyBindings()
        self.python_functions = self.get_python_functions()
        self.command_mode = True
    def read_file(self, filename):
        try:
            with open(filename, "r") as file:
                self.buffer = file.readlines()
            print(f"File '{filename}' loaded.")
        except FileNotFoundError:
            print(f"File '{filename}' not found.")
        except Exception as e:
            print(f"Error reading file: {e}")

    def get_python_functions(self):
        functions = [f for f in dir(builtins) if callable(getattr(builtins, f))]
        return functions

    def edit(self):
        print("Py-OS Text editor. Type ':q' to quit.")
        while True:
            self.render()
            completer_words = [':q', ':w', ':e', ':r', '()', "''", '[]',
                               '{}'] + self.python_functions
            if self.command_mode:
                user_input = prompt("(Command Mode) >", complete_style=CompleteStyle.COLUMN,
                                    key_bindings=self.key_bindings)
            else:
                user_input = prompt("(Insert Mode) >", completer=WordCompleter(completer_words, ignore_case=True),
                                    complete_style=CompleteStyle.COLUMN, key_bindings=self.key_bindings)
            if user_input == ":q":
                break
            elif user_input == ":w":
                self.save_to_file(input("Save as: "))
            elif user_input == ":r":
                filename = input("Enter the file name: ")
                self.read_file(filename.strip())
            elif user_input ==":e":
                self.command_mode = True
            elif user_input ==":i":
                self.command_mode = False
            else:
                self.buffer.append(user_input)

    def render(self):
        print("\033[H\033[J")
        for i, line in enumerate(self.buffer):
            if i == self.cursor_y:
                cursor_indicator = f"{' ' * self.cursor_x}"
            else:
                cursor_indicator = ''
            print(line + cursor_indicator)

    def save_to_file(self, filename):
        with open(filename, "w") as file:
            file.writelines(line + '\n' for line in self.buffer)
        print(f"File saved as '{filename}'.")

    def insert_mode(self):
        def exit_insert_mode(event):
            self.buffer.append(event.app.current_buffer.text)
            event.app.exit(result=None)

        self.key_bindings.add(Keys.Escape)

def main():
    editor = TextEditor()
    editor.edit()

if __name__ == "__main__":
    main()