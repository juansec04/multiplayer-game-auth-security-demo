import socket
import ssl
import json

HOST = "127.0.0.1"
PORT = 6000
CERT_FILE = "../certs/server.crt"


def send_request(action, username, password):
    data = {
        "action": action,
        "username": username,
        "password": password
    }

    context = ssl.create_default_context(cafile=CERT_FILE)

    with socket.create_connection((HOST, PORT)) as sock:
        with context.wrap_socket(sock, server_hostname="localhost") as secure_client:
            print("\n[SECURE CLIENT]")
            print("Sending credentials through encrypted TLS connection.")
            print("Plaintext password is not exposed on the network.")

            message = json.dumps(data)
            secure_client.sendall(message.encode())

            response = secure_client.recv(4096).decode()
            print("Server response:", response)


def main():
    print("Secure Multiplayer Game Login")
    print("1. Register")
    print("2. Login")

    choice = input("Choose an option: ")

    username = input("Username: ")
    password = input("Password: ")

    if choice == "1":
        send_request("register", username, password)
    elif choice == "2":
        send_request("login", username, password)
    else:
        print("Invalid option")


if __name__ == "__main__":
    main()