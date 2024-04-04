import requests
import sys

SERVER_URL = 'http://127.0.0.1:8888/'


def upload_file(filepath):
    files = {'file': open(filepath, 'rb')}
    response = requests.post(SERVER_URL, files=files)
    print(response.text)


def list_files():
    response = requests.get(SERVER_URL)
    print(response.text)


if __name__ == '__main__':
    if sys.argv[1] == 'upload':
        upload_file(sys.argv[2])
    elif sys.argv[1] == 'list':
        list_files()
    else:
        print("Invalid command")
