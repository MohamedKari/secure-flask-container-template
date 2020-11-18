# See https://www.docker.com/blog/how-to-use-the-official-nginx-docker-image/
FROM certbot/certbot:latest

COPY certbot-initial-entrypoint.sh certbot-initial-entrypoint.sh

ENTRYPOINT sh ./certbot-initial-entrypoint.sh