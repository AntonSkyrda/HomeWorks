import subprocess
import os

def copy_file(source, destination):
    subprocess.run(['cp', source, destination])

def prepend_to_file(file_path, content):
    with open(file_path, 'r+') as file:
        original_content = file.read()
        file.seek(0)
        file.write(content + '\n' + original_content)

def change_permissions(file_path):
    subprocess.run(['chmod', '700', file_path])

def run_file(file_path):
    subprocess.run(['python3', file_path])

def main():
    source_file = 'dz1.py'
    destination_file = 'dz1_run.py'
    prepend_text = "#!/usr/bin/env python3\n# This file is auto-generated."

    if not os.path.exists(source_file):
        print(f"File {source_file} not found.")
        return

    copy_file(source_file, destination_file)
    print(f"File {source_file} copied to {destination_file}.")

    prepend_to_file(destination_file, prepend_text)
    print(f"Text added to begin of file{destination_file}.")

    change_permissions(destination_file)
    print(f"Permissions to {destination_file} was changed.")

    print(f"Run {destination_file}:")
    run_file(destination_file)

if __name__ == "__main__":
    main()
