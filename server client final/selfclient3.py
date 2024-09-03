import socket
import os

def upload_file(s, filename):
    try:
        with open(filename, 'rb') as file:
            s.sendall(f'UPLOAD {filename}'.encode())
            while chunk := file.read(1024):
                s.sendall(chunk)
            s.sendall(b'')

            response = s.recv(1024).decode()
            print(f"Server response: {response}")
    except FileNotFoundError:
        print(f"Error: File {filename} not found.")

def download_file(s, filename):
    s.sendall(f'DOWNLOAD {filename}'.encode())
    response = s.recv(1024).decode()
    if response == 'FILE_FOUND':
        with open(filename, 'wb') as file:
            while True:
                data = s.recv(1024)
                if data.endswith(b'FILE_TRANSFER_COMPLETE'):
                    file.write(data[:-len(b'FILE_TRANSFER_COMPLETE')])
                    break
                file.write(data)
        print(f"{filename} downloaded successfully")
    else:
        print(f"Server response: {response}")

def main():
    HOST = "10.0.0.11"  
    PORT = 10000  

    while True:
        print("\nChoose an option:")
        print("1. Upload a file")
        print("2. Download a file")
        print("3. Exit")

        choice = input("Enter your choice (1/2/3): ")
        
        if choice == '3':
            print("Exiting...")
            break

        filename = input("Enter the filename: ")

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            
            if choice == '1':
                upload_file(s, filename)
            elif choice == '2':
                download_file(s, filename)
            else:
                print("Invalid choice. Please select 1 or 2.")

if __name__ == "__main__":
    main()
