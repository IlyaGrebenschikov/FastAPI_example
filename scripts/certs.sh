#!/bin/bash

mkdir -p .certs
cd .certs

openssl genrsa -out jwt-private.pem 2048
openssl rsa -in jwt-private.pem -outform PEM -pubout -out jwt-public.pem

cd ..

echo 'The keys were successfully created'
