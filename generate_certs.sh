#!/bin/bash

mkdir -p certs

openssl req -x509 \
  -newkey rsa:2048 \
  -keyout certs/server.key \
  -out certs/server.crt \
  -days 365 \
  -nodes \
  -subj "/CN=localhost"

echo "TLS certificate and key generated in the certs folder."