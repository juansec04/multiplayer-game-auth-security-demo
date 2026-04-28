import socket
import ssl
import json
import os
import hashlib
import secrets

HOST = "127.0.0.1"
PORT = 6000
USER_FILE = "users_secure.json"

CERT_FILE = "../certs/server.crt"
KEY_FILE = "../certs/server.key"

ITERATIONS = 100000


def load_users():
    if not os.path.exists(USER_FILE):
        return {}

    with open(USER_FILE, "r") as file:
        return json.load(file)


def save_users(users):
    with open(USER_FILE, "w") as file:
        json.dump(users, file, indent=4)


def hash_password(password, salt=None):
    if salt is None:
        salt = secrets.token_hex(16)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(),
        salt.encode(),
        ITERATIONS
    ).hex()

    return salt, password_hash


def verify_password(password, stored_salt, stored_hash):
    _, new_hash = hash_password(password, stored_salt)
    return secrets.compare_digest(new_hash, stored_hash)


def handle_request(data):
    users = load_users()

    action = data.get("action")
    username = data.get("username")
    password = data.get("password")

    print("\n[SECURE SERVER LOG]")
    print(f"Received request for username: {username}")
    print("Password was sent through TLS and is not printed.")

    if action == "register":
        if username in users:
            return {"status": "error", "message": "User already exists"}

        salt, password_hash = hash_password(password)

        users[username] = {
            "salt": salt,
            "password_hash": password_hash,
            "iterations": ITERATIONS
        }

        save_users(users)

        return {
            "status": "success",
            "message": "User registered securely"
        }

    elif action == "login":
        if username not in users:
            return {"status": "error", "message": "User not found"}

        stored_user = users[username]

        if verify_password(
            password,
            stored_user["salt"],
            stored_user["password_hash"]
        ):
            return {"status": "success", "message": "Secure login successful"}

        return {"status": "error", "message": "Invalid password"}

    return {"status": "error", "message": "Invalid action"}


def start_server():
    print("Secure authentication server running...")
    print(f"Listening on {HOST}:{PORT}")
    print("Using TLS encryption and salted password hashing.")

    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile=CERT_FILE, keyfile=KEY_FILE)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((HOST, PORT))
        server.listen()

        with context.wrap_socket(server, server_side=True) as secure_server:
            while True:
                conn, addr = secure_server.accept()

                with conn:
                    print(f"\nSecure TLS connection from {addr}")

                    raw_data = conn.recv(4096).decode()

                    try:
                        data = json.loads(raw_data)
                        response = handle_request(data)
                    except Exception as e:
                        response = {
                            "status": "error",
                            "message": str(e)
                        }

                    conn.sendall(json.dumps(response).encode())


if __name__ == "__main__":
    start_server()