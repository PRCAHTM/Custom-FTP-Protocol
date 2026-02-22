import socket
import json

def send_request(command):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('localhost', 20021))
    client.send(command.encode())
    response = client.recv(4096).decode()
    response_data = json.loads(response)
    print("Response from server:", response_data)
    client.close()
    return response_data

def send_data(filename, port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('localhost', port))
    with open(filename, 'rb') as file:
        while True:
            data = file.read(1024)
            if not data:
                break
            client.sendall(data)
    client.close()

def receive_data(filename, port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('localhost', port))
    with open(filename, 'wb') as file:
        while True:
            data = client.recv(1024)
            if not data:
                break
            file.write(data)
    client.close()

def main():
    while True:
        command = input("ftp> ")
        if command.lower() == "quit":
            send_request(json.dumps({"Cmd": "QUIT"}))
            break
        elif command.startswith("auth"):
            _, user, password = command.split()
            send_request(json.dumps({"Cmd": "AUTH", "User": user, "Password": password}))
        elif command.startswith("ls"):
            response = send_request(json.dumps({"Cmd": "LIST"}))
            if response["StatusCode"] == 150:
                receive_data("file_list.txt", response["DataPort"])
                with open("file_list.txt", "r") as file:
                    print(file.read())
            print("{StatusCode : 226 ,Description :  Directory send OK }")
        elif command.startswith("get"):
            _, filename = command.split()
            response = send_request(json.dumps({"Cmd": "GET", "FileName": filename}))
            if response["StatusCode"] == 150:
                receive_data(filename, response["DataPort"])
                print("Response from server: {StatusCode : 226 ,Description :  Transfer complete }")
        elif command.startswith("put"):
            _, filename = command.split()
            response = send_request(json.dumps({"Cmd": "PUT", "FileName": filename}))
            if response["StatusCode"] == 150:
                send_data(filename, response["DataPort"])
                print("Response from server: {StatusCode : 226 ,Description :  Transfer complete }")
        elif command.startswith("dele"):
            _, filename = command.split()
            send_request(json.dumps({"Cmd": "DELE", "FileName": filename}))
        elif command.startswith("mput"):
            filenames = command.split()[1:]
            filenames = filenames[0].split(",")
            response = send_request(json.dumps({"Cmd": "MPUT", "FileNames": filenames}))
            if response["StatusCode"] == 150:
                for filename in filenames:
                    send_data(filename, response["DataPort"])
                    print(f"Response from server: Filename :{filename} StatusCode : 226 ,Description :  Transfer complete ")
        else:
            print("Invalid command")

if __name__ == "__main__":
    main()
