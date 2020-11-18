Make sure your server is reachable under your domain name and has Docker and Docker Compose installed. 

Then, to spin up a Flask container serving an API securely over HTTPS, run:
```sh
# On the remote host (e. g. via SSH)
git clone https://github.com/MohamedKari/secure-flask-container-template secure_flask && cd secure_flask
echo DOMAIN_NAME=$DOMAIN_NAME >> .env 
echo EMAIL_ADDRESS=$EMAIL_ADDRESS >> .env
docker-compose -f docker-compose.initial.yml up --build # obtains the initial certificate using certbot
docker-compose up --build # runs Nginx, your app, and an auto-renewal certbot

# On your developer machine
curl https://$DOMAIN_NAME/square/5
```

That's it. Now, you're serving your containerized Flask API over HTTPS.

Modify the Flask app in `app/app.py` to your wishes and redeploy the setup with
```sh
docker-compose down
docker-compose up --build
```
