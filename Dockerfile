FROM python:3.10.13-alpine3.18

MAINTAINER Dohyung Kim

# project 파일
WORKDIR /etc/openvpn
COPY src src
COPY main.py main.py
COPY requirements.txt requirements.txt
COPY /credentials/surfshark_credentials.conf /etc/openvpn/
COPY /external-files/configurations.zip configurations.zip
RUN mkdir external-files
RUN mkdir external-files/logs
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
CMD unzip configurations.zip -d configurations;\
    # 랜덤한 프록시 선택
    CONFIG="$(find configurations -type f | shuf -n 1)";\
    # openvpn 실행
    openvpn --config ${CONFIG} --auth-user-pass surfshark_credentials.conf --daemon;\
    # 인터넷 연결 대기
    sleep 15;\
    curl icanhazip.com;\
    # 시작
    python main.py;\
