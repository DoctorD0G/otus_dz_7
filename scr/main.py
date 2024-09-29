import socket
import threading
import os

HOST = 'localhost'
PORT = 8080
DOCUMENT_ROOT = './template'


def handle_request(client_socket):
    try:
        request = client_socket.recv(1024).decode('utf-8')
        headers = request.split('\r\n')
        method, path, _ = headers[0].split(' ')

        if path == '/':
            path = '/index.html'
        file_path = DOCUMENT_ROOT + path

        if method in ['GET', 'HEAD']:
            if os.path.exists(file_path):
                with open(file_path, 'rb') as f:
                    body = f.read()
                response_headers = [
                    'HTTP/1.1 200 OK',
                    f'Content-Length: {len(body)}',
                    'Content-Type: text/html',
                    'Connection: close'
                ]
                response = '\r\n'.join(response_headers) + '\r\n\r\n'

                if method == 'GET':
                    client_socket.sendall(response.encode('utf-8') + body)
                else:
                    client_socket.sendall(response.encode('utf-8'))
            else:
                response = 'HTTP/1.1 404 Not Found\r\nConnection: close\r\n\r\n'
                client_socket.sendall(response.encode('utf-8'))
        else:
            response = 'HTTP/1.1 405 Method Not Allowed\r\nConnection: close\r\n\r\n'
            client_socket.sendall(response.encode('utf-8'))

    finally:
        client_socket.close()


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f'Server running on {HOST}:{PORT}')

    while True:
        client_socket, addr = server_socket.accept()
        print(f'Connection from {addr}')
        thread = threading.Thread(target=handle_request, args=(client_socket,))
        thread.start()


if __name__ == "__main__":
    start_server()
