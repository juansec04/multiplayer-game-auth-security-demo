Overview:
This project demonstrates a simplified authentication system for an online multiplayer game in two different states: an insecure version and a secure version. The goal is to show common vulnerabilities and how proper security mechanisms prevent attacks.


Insecure Version (Broken State)

Location: insecure_demo

This version uses plain TCP communication and stores user credentials in plaintext. Usernames and passwords are sent without encryption and saved directly in a file.

Vulnerabilities:

Credentials can be intercepted during transmission
Passwords are exposed if the database is leaked
No protection for sensitive data

Secure Version (Fixed State)
Location: secure_demo/

This version improves security by implementing TLS encryption and salted password hashing (PBKDF2). Passwords are never stored in plaintext and communication is encrypted.

Improvements:

Data is encrypted during transmission using TLS
Passwords are stored as salted hashes
Even if the database is leaked, passwords are protected

Learning Objective
This project demonstrates the difference between insecure and secure authentication systems. It highlights how attackers can exploit weak implementations and how security mechanisms mitigate those risks.

How to Run the Project

Insecure Version:

Open a terminal
Navigate to insecure_demo
Run the server: python3 server.py
Open another terminal
Run the client: python3 client.py

Secure Version:

Generate TLS certificates: ./generate_certs.sh
Navigate to secure_demo
Run the server: python3 server.py
Open another terminal
Run the client: python3 client.py

Demonstration Steps

Insecure Demo:

Register a user
Observe that the password appears in plaintext
Check users.json and see passwords stored directly

Secure Demo:

Register a user
Check users_secure.json
Observe that only a salt and hashed password are stored
Communication is encrypted

Project Structure

multiplayer-game-auth-security-demo/
insecure_demo/
server.py
client.py
users.json

secure_demo/
server.py
client.py
users_secure.json

generate_certs.sh
README.md

Security Concepts Demonstrated

Plaintext password vulnerability
Credential interception
TLS encryption
Salted password hashing (PBKDF2)

Notes
This is a minimal demonstration system. The goal is to illustrate the attack scenario and the security solution, not to build a full application.

Authors: 
Michel St. Remy
Juan Ramirez