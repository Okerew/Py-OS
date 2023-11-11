#code_runner.py
import os
import subprocess
def execute_sandboxed_code(code, language):
    if language == "python":
        return execute_python_sandboxed(code)
    elif language == "c":
        return execute_c_sandboxed(code)
    elif language == "java":
        return execute_java_sandboxed(code)
    elif language == "exe":
        return execute_exe_sandboxed(code)
    elif language == "net":
        return execute_net_sandboxed(code)
    elif language == "rust":
        return execute_rust_sandboxed(code)

def execute_python_sandboxed(code):
    try:
        exec(code, {})
        return "Code executed successfully."
    except Exception as e:
        return f"Error executing Python code: {e}"

def execute_c_sandboxed(code):
    with open("temp.c", "w") as f:
        f.write(code)

    try:
        subprocess.run(["gcc", "temp.c", "-o", "temp"], check=True)
        result = subprocess.run(["./temp"], stdout=subprocess.PIPE, text=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error compiling or running C code: {e}"

def execute_java_sandboxed(code):
    with open("Temp.java", "w") as f:
        f.write(code)

    try:
        subprocess.run(["javac", "Temp.java"], check=True)
        result = subprocess.run(["java", "Temp"], stdout=subprocess.PIPE, text=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error compiling or running Java code: {e}"

def execute_exe_sandboxed(exe_path):
    try:
        result = subprocess.run([exe_path], stdout=subprocess.PIPE, text=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error running the .exe file: {e}"

def execute_net_sandboxed(code):
    try:
        with open("temp.cs", "w") as f:
            f.write(code)
        result = subprocess.run(["dotnet", "run", "--no-build", "--project", "temp.csproj"], stdout=subprocess.PIPE, text=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error running .NET code: {e}"

def execute_rust_sandboxed(code):
    try:
        with open("temp.rs", "w") as f:
            f.write(code)
        subprocess.run(["rustc", "temp.rs", "-o", "temp"], check=True)
        result = subprocess.run(["./temp"], stdout=subprocess.PIPE, text=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error compiling or running Rust code: {e}"

def execute_code(language, code):
    if language not in ["python", "c", "java", "exe", "net", "rust"]:
        return "Unsupported language."

    result = execute_sandboxed_code(code, language)
    return result

def find_files_with_extension(root_dir, extension):
    found_files = []
    for root, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith(extension):
                found_files.append(os.path.join(root, file))
    return found_files

def main():
    execution_option = input("Choose an option:\n1. Execute code from a file\n2. Execute code directly\n3. quit\n")

    if execution_option == "1":
        language = input("Enter a programming language (python, c, java, exe, net, rust): ")
        extension_mapping = {
            "python": ".py",
            "c": ".c",
            "java": ".java",
            "exe": ".exe",
            "net": ".cs",
            "rust": ".rs"
        }

        if language not in extension_mapping:
            print("Unsupported language.")
            return

        root_folder = os.getcwd()  # Get the current working directory as the root folder
        file_extension = extension_mapping[language]
        matching_files = find_files_with_extension(root_folder, file_extension)

        if not matching_files:
            print(f"No {language} files found in the specified folder and its subfolders.")
            return

        print(f"Found {len(matching_files)} {language} files:")
        for i, file_path in enumerate(matching_files, start=1):
            print(f"{i}. {file_path}")

        file_number = int(input("Select a file number to execute: ")) - 1

        try:
            if language in ["exe", "net", "rust"]:
                selected_file = matching_files[file_number]
            else:
                with open(matching_files[file_number], "r") as f:
                    code = f.read()
        except IndexError:
            print("Invalid file number.")
            return
        except FileNotFoundError:
            print("Selected file not found.")
            return

    elif execution_option == "2":
        language = input("Enter a programming language (python, c, java, exe, net, rust): ")
        if language in ["exe", "net", "rust"]:
            selected_file = input(f"Enter the path to the {language} file: ")
        else:
            code = input("Enter the code:\n")
    elif execution_option =="3":
        print("Exiting...")
        return

    else:
        print("Invalid option.")
        return

    if language in ["exe", "net", "rust"]:
        output = execute_code(language, selected_file)
    else:
        output = execute_code(language, code)
    print(output)

if __name__ == "__main__":
    main()
