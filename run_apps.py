# run_apps.py

import os

def list_apps():
    app_files = [filename[:-3] for filename in os.listdir("apps") if filename.endswith(".py")]
    return app_files

def generate_commands():
    apps = list_apps()
    commands = {app: f"Run the {app} app" for app in apps}
    return commands

commands = generate_commands()

def run_app(app_name):
    try:
        module = __import__(f"apps.{app_name}", fromlist=[None])
        module.main()
    except ImportError:
        print(f"App '{app_name}' not found.")
    except Exception as e:
        print(f"An error occurred while running '{app_name}': {e}")

def run_specific_app(app_name):
    run_app(app_name)
