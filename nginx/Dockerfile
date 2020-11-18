# See https://www.docker.com/blog/how-to-use-the-official-nginx-docker-image/
FROM nginx:latest

RUN rm /etc/nginx/conf.d/default.conf


# As indicated here (https://github.com/docker-library/docs/tree/master/nginx#using-environment-variables-in-nginx-configuration-new-in-119)
# Nginx will load all *.template files from /etc/nginx/templates/,
# envsubst them (we inject the domain name as an environment variable),
# and write them out as conf.d
COPY nginx-https.conf.template /etc/nginx/templates/
COPY nginx-entrypoint.sh nginx-entrypoint.sh

ENTRYPOINT bash ./nginx-entrypoint.sh