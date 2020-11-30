# HTTPS-secured APIs with Docker

_A template repo showing how to serve an API over HTTPS conveniently with Let's Encrypt certificates, using Certbot, Nginx, and - exemplarily - Flask , each running in a Docker container spun up through Docker Compose._

> This repo accompanies my blog post under https://blog.mkari.de/posts/secure-apis/.

## Quick Start

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

## Automate Deployment 
> I explained the rationale for this part in https://blog.mkari.de/posts/single-docker-host-cicd/.

```sh
echo GITHUB_TOKEN=$GITHUB_TOKEN >> .env 
echo REPO_OWNER=$REPO_OWNER >> .env
echo REPO_NAME=$REPO_NAME >> .env
echo DOCKER_MACHINE_NAME=$DOCKER_MACHINE_NAME >> .env

python -m venv .gh-secrets
source .gh-secrets/bin/activate
pip install -r gh-secrets/requirements.txt

eval $(cat .env |grep "^[^#]")
python gh-secrets/gh-secrets.py deploy_docker_machine_certs $REPO_OWNER $REPO_NAME $DOCKER_MACHINE_NAME
python gh-secrets/gh-secrets.py set $REPO_OWNER $REPO_NAME EMAIL_ADDRESS $EMAIL_ADDRESS
python gh-secrets/gh-secrets.py set $REPO_OWNER $REPO_NAME DOMAIN_NAME $DOMAIN_NAME
```

# FAQ
## How do I start a remote Docker host in the cloud using docker-machine?

For GCP server, I usually use something like:
```sh
docker-machine create --driver google \
    --google-disk-size 100 \
    --google-disk-type pd-standard \
    --google-project $PROJECT_NAME \
    --google-zone europe-west3-a \
    --google-machine-type e2-medium \
    --google-machine-image projects/confidential-vm-images/global/images/ubuntu-1804-bionic-v20200716 \
    --google-open-port 80,443 \
    secure-server
```