import socket
import threading
import json
import os
import time

isroot = False

def handle_client(client_socket):
    while True:
        try:
            request = client_socket.recv(1024).decode()
            if not request:
                break

            request_data = json.loads(request)
            cmd = request_data.get("Cmd")

            if cmd == "AUTH":
                user = request_data.get("User")
                password = request_data.get("Password")
                response = handle_auth(user, password)
                client_socket.send(json.dumps(response).encode())
            elif cmd == "QUIT":
                response = handle_quit()
                client_socket.send(json.dumps(response).encode())
                break
            elif cmd == "LIST":
                response = handle_list()
                client_socket.send(json.dumps(response).encode())
                if response["StatusCode"] == 150:
                    data_socket, addr = server_data_socket.accept()
                    list_directory(data_socket)
                    data_socket.close()
            elif cmd == "GET":
                filename = request_data.get("FileName")
                response = handle_get(filename)
                client_socket.send(json.dumps(response).encode())
                if response["StatusCode"] == 150:
                    data_socket, addr = server_data_socket.accept()
                    send_file(filename, data_socket)
                    data_socket.close()
            elif cmd == "PUT":
                filename = request_data.get("FileName")
                response = handle_put(filename)
                client_socket.send(json.dumps(response).encode())
                if response["StatusCode"] == 150:
                    data_socket, addr = server_data_socket.accept()
                    receive_file(filename, data_socket)
                    data_socket.close()
            elif cmd == "DELE":
                filename = request_data.get("FileName")
                response = handle_dele(filename)
                client_socket.send(json.dumps(response).encode())
            elif cmd == "MPUT":
                filenames = request_data.get("FileNames", [])
                response = handle_mput(filenames)
                client_socket.send(json.dumps(response).encode())
                if response["StatusCode"] == 150:
                    data_socket, addr = server_data_socket.accept()
                    for filename in filenames:
                        receive_file(filename, data_socket)
                    data_socket.close()
            else:
                response = {"StatusCode": 400, "Description": "Invalid Command"}
                client_socket.send(json.dumps(response).encode())
        except Exception as e:
            print(f"Error: {e}")
            break

    client_socket.close()

def handle_auth(user, password):
    global isroot
    if user == "admin" and password == "password":
        isroot = True
        return {"StatusCode": 230, "Description": "Successfully logged in. Proceed"}
    else:
        return {"StatusCode": 430, "Description": "Failure in granting root accessibility"}

def handle_quit():
    return {"StatusCode": 200, "Description": "Connection closed"}

def handle_list():
    files = os.listdir('.')
    if files:
        return {"StatusCode": 150, "Description": "PORT command successful", "DataPort": 20020}
    else:
        return {"StatusCode": 210, "Description": "Empty"}

def handle_get(filename):
    if os.path.exists(filename):
        return {"StatusCode": 150, "Description": "OK to send data", "DataPort": 20020}
    else:
        return {"StatusCode": 550, "Description": "File doesn't exist"}

def handle_put(filename):
    if isroot:
        return {"StatusCode": 150, "Description": "OK to send data", "DataPort": 20020}
    else:
        return {"StatusCode": 434, "Description": "The client doesn’t have the root access. File transfer aborted."}

def handle_dele(filename):
    if isroot:
        if os.path.exists(filename):
            os.remove(filename)
            return {"StatusCode": 200, "Description": "Successfully deleted"}
        else:
            return {"StatusCode": 550, "Description": "File doesn't exist"}
    else:
        return {"StatusCode": 434, "Description": " The client doesn't have the root access ."}

def handle_mput(filenames):
    if isroot:
        return {"StatusCode": 150, "Description": "OK to send data", "DataPort": 20020}
    else:
        return {"StatusCode": 434, "Description": "The client doesn’t have the root access. File transfer aborted."}

def list_directory(data_socket):
    files = os.listdir('.')
    file_list = "\n".join(files)
    data_socket.sendall(file_list.encode())

def send_file(filename, data_socket, max_bandwidth_kbps=100):
    max_bandwidth_bps = max_bandwidth_kbps * 1024  # Convert KB/s to Bytes/s
    with open(filename, 'rb') as file:
        total_sent = 0
        start_time = time.time()
        while True:
            data = file.read(1024)
            if not data:
                break
            data_socket.sendall(data)
            total_sent += len(data)

            elapsed_time = time.time() - start_time
            if elapsed_time > 0:
                transfer_rate = total_sent / elapsed_time
                if transfer_rate > max_bandwidth_bps:
                    sleep_time = (total_sent / max_bandwidth_bps) - elapsed_time
                    time.sleep(sleep_time)

            file_size = os.path.getsize(filename)
            progress = (total_sent / file_size) * 100
            print(f"Progress: {progress:.2f}% - Transfer Rate: {transfer_rate / 1024:.2f} KB/s")

def receive_file(filename, data_socket):
    with open(filename, 'wb') as file:
        while True:
            data = data_socket.recv(1024)
            if not data:
                break
            file.write(data)

def main():
    global server_data_socket
    server_data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_data_socket.bind(('localhost', 20020))
    server_data_socket.listen(5)
    print("Data socket listening on port 20020")

    server_control_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_control_socket.bind(('localhost', 20021))
    server_control_socket.listen(5)
    print("Control socket listening on port 20021")

    while True:
        client_socket, addr = server_control_socket.accept()
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    main()
