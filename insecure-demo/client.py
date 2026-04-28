import argparse
import socket
import json
import os

HOST = "127.0.0.1"
DEFAULT_PORT = 5000


def send_request(action, username, password, host, port):
    data = {
        "action": action,
        "username": username,
        "password": password
    }

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((host, port))

        message = json.dumps(data)

        print("\n[INSECURE CLIENT]")
        print(f"Sending plaintext data: {message}")

        client.sendall(message.encode())

        response = client.recv(4096).decode()
        print("Server response:", response)


def parse_args():
    parser = argparse.ArgumentParser(description="Run the insecure demo client")
    parser.add_argument("--host", default=HOST, help="Server host")
    parser.add_argument(
        "--port",
        type=int,
        default=int(os.getenv("PORT", DEFAULT_PORT)),
        help="Server port",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    print("Insecure Multiplayer Game Login")
    print("1. Register")
    print("2. Login")

    choice = input("Choose an option: ")

    username = input("Username: ")
    password = input("Password: ")

    if choice == "1":
        send_request("register", username, password, args.host, args.port)
    elif choice == "2":
        send_request("login", username, password, args.host, args.port)
    else:
        print("Invalid option")


if __name__ == "__main__":
    main()