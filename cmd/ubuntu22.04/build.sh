SERVER_PROJECT_LOCATION=/home/ubuntu/projects
PROJECT_NAME=appiumScraper

unzip_project() {
  cd ${SERVER_PROJECT_LOCATION}
  rm -f -r ${PROJECT_NAME}
  mkdir ${PROJECT_NAME}
  unzip ${PROJECT_NAME}.zip -d ${SERVER_PROJECT_LOCATION}/${PROJECT_NAME}
  rm -f ${PROJECT_NAME}.zip
}

unzip_project
cd ${PROJECT_NAME}
docker build -t appium-scraper .
