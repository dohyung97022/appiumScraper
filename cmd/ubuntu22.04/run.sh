SERVER_PROJECT_LOCATION=/home/ubuntu/projects
PROJECT_NAME=appiumScraper

cd ${SERVER_PROJECT_LOCATION}/${PROJECT_NAME}
# kompose 로 생성된 kubernetes deployment 적용
sudo kubectl apply -f appium-scraper-deployment.yaml,appium-scraper-service.yaml
# deployment 재시작
sudo kubectl rollout restart deployment appium-scraper