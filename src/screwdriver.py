import requests
import sys

SERVER_URL = 'http://127.0.0.1:8888/'


def upload_file(filepath):
    try:
        with open(filepath, 'rb') as f:
            files = {'file': f}
            response = requests.post(SERVER_URL + 'api/upload', files=files)
            if response.ok:
                print(response.json().get("message", "File uploaded successfully"))
                list_files()
            else:
                print(response.json().get("error", "Error uploading the file"))
    except FileNotFoundError:
        print(f"Error: The file '{filepath}' was not found.")


def list_files():
    response = requests.get(SERVER_URL + 'api/files')
    if response.ok:
        files = response.json()
        for file in files:
            print(file)
    else:
        print("Error retrieving the list of files")


if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == 'upload' and len(sys.argv) == 3:
            upload_file(sys.argv[2])
        elif sys.argv[1] == 'list':
            list_files()
        else:
            print("Invalid command or missing arguments")
    else:
        print("Please provide a command")
