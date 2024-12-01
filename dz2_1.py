import subprocess
import os
from datetime import datetime, timedelta
import random

def get_current_user():
    result = subprocess.run(['whoami'], capture_output=True, text=True)
    return result.stdout.strip()

def get_current_directory():
    result = subprocess.run(['pwd'], capture_output=True, text=True)
    return result.stdout.strip()

def create_directory(directory_name):
    os.makedirs(directory_name, exist_ok=True)

def generate_file_names(month, year):
    num_days = (datetime(year, month + 1, 1) - timedelta(days=1)).day if month < 12 else 31
    return [
        f"{day:02d}-{month:02d}-{year}.log" for day in range(1, num_days + 1)
    ]

def create_files_in_directory(directory, file_names):
    for file_name in file_names:
        file_path = os.path.join(directory, file_name)
        open(file_path, 'w').close()

def change_owner(directory):
    subprocess.run(['sudo', 'chown', '-R', 'root:root', directory])

def delete_random_files(directory, count=5):
    files = os.listdir(directory)
    files_to_delete = random.sample(files, min(len(files), count))
    for file_name in files_to_delete:
        os.remove(os.path.join(directory, file_name))

def main():
    print(f"Current user name: {get_current_user()}")
    print(f"Current dir: {get_current_directory()}")

    current_directory = get_current_directory()
    target_directory = os.path.join(current_directory, 'dz1')

    create_directory(target_directory)
    print(f"Dir {target_directory} created.")

    today = datetime.now()
    file_names = generate_file_names(today.month, today.year)
    create_files_in_directory(target_directory, file_names)
    print(f"Files created in dir {target_directory}.")

    change_owner(target_directory)
    print(f"Dir owner {target_directory} and files were changed to root.")

    delete_random_files(target_directory)
    print("5 random files were deleted.")

if __name__ == "__main__":
    main()
