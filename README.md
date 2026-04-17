Overview:
This project demonstrates a simplified authentication system for an online multiplayer game in two different states: an insecure version and a secure version. The goal is to show common vulnerabilities and how proper security mechanisms prevent attacks.


Insecure Version (Broken State)

Location: insecure_demo

This version uses plain TCP communication and stores user credentials in plaintext. Usernames and passwords are sent without encryption and saved directly in a file.
