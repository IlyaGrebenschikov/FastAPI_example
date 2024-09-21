mkdir .certs
Set-Location .certs

& openssl genrsa -out jwt-private.pem 2048
& openssl rsa -in jwt-private.pem -outform PEM -pubout -out jwt-public.pem

Set-Location ..

Write-Host 'The keys were successfully created'
