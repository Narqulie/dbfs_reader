import requests
import os
import base64
import polars as pl
from io import StringIO
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

# Load the access token and Databricks instance URL from the environment variables
ACCESS_TOKEN = os.environ.get('DATABRICKS_ACCESS_TOKEN')
ACCESS_TOKEN = f"Bearer {ACCESS_TOKEN}"
DATABRICKS_INSTANCE = os.environ.get('DATABRICKS_INSTANCE')
BASE_PATH = 'dbfs:/'

# Set up the headers for the API requests
headers = {
    'Authorization': ACCESS_TOKEN
}

list_url = f"{DATABRICKS_INSTANCE}/api/2.0/dbfs/list"
download_url = f"{DATABRICKS_INSTANCE}/api/2.0/dbfs/read"


def list_files(path):
    response = requests.get(list_url, headers=headers, json={'path': path})
    if response.status_code == 200:
        items = response.json().get('files', [])
        for idx, item in enumerate(items, start=1):
            if item['is_dir']:
                print(f"{idx}. Directory: {item['path']}")
            else:
                print(f"{idx}. File: {item['path']} (Size: {item['file_size']} bytes)")
        return items
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return []


def preview_file(path):
    response = requests.get(download_url, headers=headers, json={'path': path})
    if response.status_code == 200:
        file_content = base64.b64decode(response.json().get('data', '')).decode('utf-8')
        df = pl.read_csv(StringIO(file_content))
        print(f"File {path} content:\n")
        print(df)
        return file_content
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None


def download_file(path, content):
    local_filename = os.path.basename(path)
    local_path = os.path.join(os.getcwd(), 'downloaded', local_filename)
    os.makedirs(os.path.dirname(local_path), exist_ok=True)
    with open(local_path, 'w') as file:
        file.write(content)
    print(f"File {path} downloaded successfully to {local_path}.")


def main():
    current_path = BASE_PATH
    while True:
        print(f"\nListing contents of {current_path}:\n")
        items = list_files(current_path)
        
        if not items:
            continue
        
        next_step = input("\nEnter the number to navigate into (or '..' to go up, 'exit' to quit): ").strip()
        
        if next_step in ("exit", "quit", "bye"):
            break
        elif next_step == '..':
            if current_path != BASE_PATH:
                current_path = '/'.join(current_path.rstrip('/').split('/')[:-1])
                if not current_path.endswith('/'):
                    current_path += '/'
        else:
            try:
                index = int(next_step) - 1
                if 0 <= index < len(items):
                    selected_item = items[index]
                    if selected_item['is_dir']:
                        current_path = selected_item['path']
                        if not current_path.endswith('/'):
                            current_path += '/'
                    else:
                        file_content = preview_file(selected_item['path'])
                        if file_content:
                            download_choice = input("Do you want to download this file? (yes/no): ").strip().lower()
                            if download_choice in ('yes', 'y', '1'):
                                download_file(selected_item['path'], file_content)
                else:
                    print("Invalid number. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a number.")

if __name__ == "__main__":
    main()