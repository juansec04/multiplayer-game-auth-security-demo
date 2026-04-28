import argparse
import socket
import json
import os

HOST = "127.0.0.1"
DEFAULT_PORT = 5000
USER_FILE = "users.json"


def load_users():
    if not os.path.exists(USER_FILE):
        return {}

    with open(USER_FILE, "r") as file:
        return json.load(file)


def save_users(users):
    with open(USER_FILE, "w") as file:
        json.dump(users, file, indent=4)


def handle_request(data):
    users = load_users()

    action = data.get("action")
    username = data.get("username")
    password = data.get("password")

    print("\n[INSECURE SERVER LOG]")
    print(f"Received username: {username}")
    print(f"Received password: {password}")

    if action == "register":
        if username in users:
            return {"status": "error", "message": "User already exists"}

        users[username] = {
            "password": password
        }

        save_users(users)
        return {"status": "success", "message": "User registered insecurely"}

    elif action == "login":
        if username not in users:
            return {"status": "error", "message": "User not found"}

        if users[username]["password"] == password:
            return {"status": "success", "message": "Login successful"}

        return {"status": "error", "message": "Invalid password"}

    return {"status": "error", "message": "Invalid action"}


def parse_args():
    parser = argparse.ArgumentParser(description="Run the insecure authentication server")
    parser.add_argument("--host", default=HOST, help="Server host")
    parser.add_argument(
        "--port",
        type=int,
        default=int(os.getenv("PORT", DEFAULT_PORT)),
        help="Server port",
    )
    return parser.parse_args()


def start_server(host, port):
    print("Insecure authentication server running...")
    print(f"Listening on {host}:{port}")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((host, port))
        server.listen()

        while True:
            conn, addr = server.accept()

            with conn:
                print(f"\nConnection from {addr}")

                raw_data = conn.recv(4096)
                if not raw_data:
                    continue

                raw_data = raw_data.decode()
                print(f"Raw data received: {raw_data}")

                try:
                    data = json.loads(raw_data)
                    response = handle_request(data)
                except json.JSONDecodeError:
                    response = {"status": "error", "message": "Invalid JSON"}
                except Exception as e:
                    response = {"status": "error", "message": str(e)}

                conn.sendall(json.dumps(response).encode())


if __name__ == "__main__":
    args = parse_args()
    start_server(args.host, args.port)