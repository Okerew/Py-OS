# main.py
import os
import getpass
try:
    from core_commands import CoreCommands
    from run_apps import commands, run_specific_app
    import bs4
except ModuleNotFoundError:
    with open("requirements.txt", "r") as file:
        libraries = file.read().splitlines()
        for library in libraries:
            library = library.strip()
            if library:
                os.system(f"pip install {library} --quiet")
    from core_commands import CoreCommands
    from run_apps import commands, run_specific_app

def main():
    print(",-.----.                         ,----..               ")
    print("\    /  \                       /   /   \   .--.--.    ")
    print("|   :    \                     /   .     : /  /    '. ")
    print("|   |  .\ :            ,---,. .   /   ;.  \  :  /`. / ")
    print(".   :  |: |          ,'  .' |.   ;   /  ` ;  |  |--`  ")
    print("|   |   \ :    .--,,---.'   ,;   |  ; \ ; |  :  ;_     ")
    print("|   : .   /  /_ ./||   |    ||   :  | ; | '\  \    `.  ")
    print("|   | |`-'   | |||   |    ||   |  ;  \: |  `----.   \ ")
    print("|   | ;  /___/ \: |:   |.'   '   ;  \; /  | __ \  \  | ")
    print(":   ' |   .  \  ' |`---'      \   \  ',  / /  /`--'  /")
    print("   : :    \  ;   :            ;   :    / '--'.     /")
    print("|   | :     \  \  ;             \   \ .'    `--'---'")
    print("`---'.|      :  \  \             `---`                ")
    print("  `---`       \  ' ;                                   ")
    print("               `--`                                   ")

    print("Please login or create a new user (create_user)")
    core = CoreCommands()

    while True:
        user_input = input(">")
        if user_input in commands:
            if user_input == "apps":
                print("Available apps:")
                for command, app_name in commands.items():
                    print(f"{command} - {app_name}")
            else:
                run_specific_app(user_input)
        else:
            if core.logged_in_user is None:
                if user_input == "create_user":
                    username = input("Enter your username: ")
                    password = getpass.getpass("Enter your password: ")
                    core.create_user(username, password)
                elif user_input == "login":
                    username = input("Enter your username: ")
                    password = getpass.getpass("Enter your password: ")
                    core.login(username, password)
                else:
                    print("You must be logged in or create a user")
            else:
                core.run_command(user_input)

if __name__ == "__main__":
    main()
