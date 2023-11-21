docker build -t appium_scraper .
docker run --privileged --dns 8.8.8.8 --cap-add=NET_ADMIN --device /dev/net/tun:/dev/net/tun -it appium_scraper
