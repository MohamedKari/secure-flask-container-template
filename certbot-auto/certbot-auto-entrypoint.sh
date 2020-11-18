# First set of certificates

while true; do
    sleep 1m & wait ${!};

    certbot certonly \
        --webroot -w /var/www/certbot \
        -d $DOMAIN_NAME \
        -m $EMAIL_ADDRESS \
        --rsa-key-size "2048" \
        --agree-tos \
        -n
done
