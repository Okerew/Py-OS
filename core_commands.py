# core_commands.py
import shutil
import os
from run_apps import commands
import platform
import code_runner
import sys
import hashlib
import subprocess

class CoreCommands:
    def __init__(self):
        self.current_folder = os.getcwd()
        self.logged_in_user = None
        self.user_data_file = "users.pexof"
        self.commands = {
            **commands,
            "help": "Display available commands",
            "exit": "Exit the system",
            "apps": "List available apps",
            "pypi": "Install a custom python library",
            "cleaner": "Cleans the system caches should be used regularly",
            "lf": "Lists all the files in a folder",
            "git_clone": "Clones a git repository",
            "del": "Deletes a file needs to be used with lf command",
            "move": "Moves a file must be used with lf command",
            "code_runner": "Runs python, java,c scripts",
            "restart": "Restarts the system",
            "clear": "clears the terminal",
        }

    def run_command(self, command):
        if command in self.commands:
            if command == "help":
                self.show_help()
            elif command == "exit":
                self.exit()
            elif command == "apps":
                self.show_apps()
            elif command == "pypi":
                pypi_command = input("Input the thing you want to do with pip: ")
                pypi_option = input("Input an additional option: ")
                os.system(f"pip {pypi_command} {pypi_option}")
            elif command == "cleaner":
                self.clean_pyc_files()
            elif command =="lf":
                folder = input("Input the folder you want to list: ")
                self.change_folder(folder)
            elif command == "del":
                filename = input("Input the file you want to delete: ")
                self.delete_file(filename)
            elif command == "git_clone":
                repo_url = input("Input the repo url: ")
                self.git_clone(repo_url)
            elif command =="code_runner":
                code_runner.main()
            elif command == "move":
                self.move_file_using_lf()
            elif command == "restart":
                print("Restarting the system...")
                self.restart_program()
            elif command == "clear":
                self.clear_screen()
            else:
                self.run_app(command)
        else:
            print("Unknown command.")

    def show_help(self):
        print("Available commands:")
        for command, description in self.commands.items():
            print(f"{command} - {description}")

    def exit(self):
        print("Exiting the system.")
        raise SystemExit

    def show_apps(self):
        print("Available apps:")
        for command, app_name in commands.items():
            print(f"{command} - {app_name}")

    def run_app(self, app_name):
        try:
            module = __import__(f"apps.{app_name}", fromlist=[None])
            module.main()
        except ImportError:
            print(f"App '{app_name}' not found.")
        except Exception as e:
            print(f"An error occurred while running '{app_name}': {e}")

    def clean_pyc_files(self, folder="."):
        pyc_files = []

        for root, dirs, files in os.walk(folder):
            pyc_files.extend([os.path.join(root, f) for f in files if f.endswith(".pyc")])

        if pyc_files:
            print("Cleaning up .pyc files...")
            for pyc_file in pyc_files:
                if os.path.exists(pyc_file):
                    print(f"Removing {pyc_file}...")
                    os.remove(pyc_file)
                    print(f"Removed {pyc_file}")
            print("Cleaned up .pyc files.")
        else:
            print("No .pyc files found.")

    def git_clone(self, repo_url):
        if not self.logged_in_user:
            print("You must be logged in to clone a Git repository.")
            return

        try:
            user_folder = os.path.join(self.current_folder, self.logged_in_user)
            os.makedirs(user_folder, exist_ok=True)

            # Clone the Git repository inside the user's folder
            git_clone_command = f"git clone {repo_url} {user_folder}"
            subprocess.run(git_clone_command, shell=True, check=True)
            print("Git repository cloned successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error cloning Git repository: {e}")

    def change_folder(self, folder_name):
        new_folder = os.path.join(self.current_folder, folder_name)
        if os.path.exists(new_folder) and os.path.isdir(new_folder):
            self.current_folder = new_folder
            print(f"Changed to '{self.current_folder}' directory.")
            self.list_files()
        else:
            print(f"Folder '{new_folder}' does not exist.")

    def list_files(self):
        folder_contents = os.listdir(self.current_folder)
        print(f"Files and folders in '{self.current_folder}':")
        for item in folder_contents:
            print(item)

    def delete_file(self, filename):
        file_path = os.path.join(self.current_folder, filename)
        try:
            os.remove(file_path)
            print(f"File '{filename}' deleted.")
        except FileNotFoundError:
            print(f"File '{filename}' not found.")
        except Exception as e:
            print(f"Error deleting file: {e}")

    def move_file_using_lf(self):
        current_folder = os.getcwd()

        folder_name = os.path.join(self.current_folder)
        source_file = input("Enter the file name: ")
        destination_folder = input("Enter the destination folder name: ")

        source_path = os.path.join(current_folder, folder_name, source_file)
        destination_path = os.path.join(current_folder, destination_folder, source_file)

        if os.path.exists(source_path):
            shutil.move(source_path, destination_path)
            print(f"Moved '{source_file}' to '{destination_folder}'.")
        else:
            print(f"File '{source_file}' not found.")

    def restart_program(self):
        python = sys.executable
        os.execl(python, python, *sys.argv)

    def clear_screen(self):
        system_platform = platform.system()
        if system_platform == "Windows":
            os.system("cls")
        else:
            os.environ["TERM"] = "xterm"
            os.system("clear")

    def create_user(self, username, password):
        #creating the user and encoding the password
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        user_data = f"[User]\nUsername: {username}\nPassword: {hashed_password}\n\n"
        with open(self.user_data_file, "a") as file:
            file.write(user_data)

        user_folder = os.path.join(self.current_folder, username)
        os.makedirs(user_folder, exist_ok=True)
        print(f"User '{username}' created successfully with a personal folder.")

    def login(self, username, password):
        with open(self.user_data_file, "r") as file:
            user_data = file.read()
            users = user_data.split("[User]\n")[1:]
            for user in users:
                user_lines = user.strip().split("\n")
                stored_username = None
                stored_password = None
                for line in user_lines:
                    if line.startswith("Username: "):
                        stored_username = line.split(": ")[1]
                    elif line.startswith("Password: "):
                        stored_password = line.split(": ")[1]
                if stored_username is not None and stored_password is not None:
                    hashed_password = hashlib.sha256(password.encode()).hexdigest()
                    if username == stored_username and hashed_password == stored_password:
                        self.logged_in_user = username
                        print(f"Welcome, {username}!")
                        return

        print("Login failed. Please check your username and password.")
