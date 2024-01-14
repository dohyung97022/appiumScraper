FROM python:3.10.13-alpine3.18

MAINTAINER Dohyung Kim

# project 파일
WORKDIR /etc/openvpn
COPY src src
COPY main.py main.py
COPY requirements.txt requirements.txt
COPY ./credentials ./credentials
COPY ./external-files ./external-files
COPY retry.sh retry.sh
RUN mkdir ./external-files/configurations
RUN mkdir -p /dev/net && \
    mknod /dev/net/tun c 10 200 && \
    chmod 600 /dev/net/tun
# 기본 도구
RUN apk --no-cache update
RUN apk --no-cache add zip
RUN apk --no-cache add openvpn
RUN apk --no-cache add curl
# mysql 연결
RUN apk --no-cache add pkgconfig
RUN apk --no-cache add mariadb-connector-c-dev
# timezone 설치
RUN apk --no-cache add tzdata
RUN cp /usr/share/zoneinfo/Asia/Seoul /etc/localtime
# pip install
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
# openvpn 연결
WORKDIR /etc/openvpn
CMD unzip -o ./external-files/configurations.zip -d ./external-files/configurations;\
    ./retry.sh;\
