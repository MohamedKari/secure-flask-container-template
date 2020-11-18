# See https://www.docker.com/blog/how-to-use-the-official-nginx-docker-image/
FROM certbot/certbot:latest

COPY certbot-auto-entrypoint.sh certbot-auto-entrypoint.sh

ENTRYPOINT sh ./certbot-auto-entrypoint.sh