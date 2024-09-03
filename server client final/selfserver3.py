import socket
import os
import threading

HOST = "0.0.0.0"  
PORT = 10000  
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def handle_client(conn):
    try:
        while True:
            request = conn.recv(1024).decode().strip()
            if not request:
                break

            parts = request.split(maxsplit=1)
            if len(parts) < 2:
                conn.sendall(b'INVALID_REQUEST_FORMAT')
                continue

            command, filename = parts
            filename = filename.strip()

            if command == 'UPLOAD':
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                with open(file_path, 'wb') as f:
                    while True:
                        data = conn.recv(1024)
                        if not data:
                            break
                        f.write(data)
                conn.sendall(b'UPLOAD_COMPLETE')

            elif command == 'DOWNLOAD':
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                if os.path.isfile(file_path):
                    conn.sendall(b'FILE_FOUND')
                    with open(file_path, 'rb') as f:
                        while chunk := f.read(1024):
                            conn.sendall(chunk)
                    conn.sendall(b'FILE_TRANSFER_COMPLETE')
                else:
                    conn.sendall(b'FILE_NOT_FOUND')

            else:
                conn.sendall(b'INVALID_COMMAND')
    
    except socket.error as e:
        print(f"Socket error: {e}")
    finally:
        conn.close()

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Server listening on {HOST}:{PORT}")
        
        while True:
            conn, addr = s.accept()
            print(f"Connected by {addr}")
            client_thread = threading.Thread(target=handle_client, args=(conn,))
            client_thread.start()

if __name__ == "__main__":
    main()
