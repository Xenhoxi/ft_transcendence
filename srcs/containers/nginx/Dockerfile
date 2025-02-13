FROM nginx:latest

RUN apt-get update -y && apt-get upgrade -y && \
    apt-get install -y nginx vim openssl
RUN rm -f /etc/nginx/conf.d/default.conf
COPY ./conf/winx.conf /etc/nginx/conf.d

RUN mkdir -p /etc/nginx/ssl

RUN openssl req -x509 -newkey rsa:4096 -nodes -keyout /etc/nginx/ssl/key.pem -out /etc/nginx/ssl/cert.pem -days 365 \
  -subj '/C=FR/ST=ICI/L=CHEZMOI/O=NEO CO/OU=LA/CN=localhost'

EXPOSE 4443