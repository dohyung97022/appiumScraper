FROM python:3.10.13-alpine3.18

MAINTAINER Dohyung Kim

COPY /credentials/surfshark_credentials.conf /etc/openvpn/
RUN apk update
RUN apk add zip
RUN apk add openvpn

WORKDIR /etc/openvpn
CMD wget my.surfshark.com/vpn/api/v1/server/configurations;\
    unzip configurations;\
    openvpn --config kr-seo.prod.surfshark.com_udp.ovpn --daemon --auth-user-pass surfshark_credentials.conf;\
