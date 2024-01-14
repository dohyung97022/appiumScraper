PROJECT_NAME=appiumScraper

SERVER_USERNAME=ubuntu
SERVER_IP4=192.168.45.4 # ubuntu4
SERVER_PROJECT_LOCATION=/home/ubuntu/projects

compose_convert() {
  kompose convert --replicas 1
}

zip_file() {
  zip -r ${PROJECT_NAME}.zip . -x "venv/lib/*" ".git/*" ".idea/*"
}

delete_zip_file() {
  rm ${PROJECT_NAME}.zip
}

transfer_zip_file() {
  server_ip=$1
  server_username=$2
  server_project_location=$3
  scp ${PWD}/${PROJECT_NAME}.zip ${PWD}/cmd/ubuntu22.04/build.sh ${PWD}/cmd/ubuntu22.04/run.sh ${server_username}@${server_ip}:${server_project_location}
}

build() {
  server_ip=$1
  server_username=$2
  server_project_location=$3
  ssh -t ${server_username}@${server_ip} "sudo ${server_project_location}/build.sh"
}

run() {
  server_ip=$1
  server_username=$2
  server_project_location=$3
  ssh -t ${server_username}@${server_ip} "${server_project_location}/run.sh"
}

compose_convert
zip_file
transfer_zip_file ${SERVER_IP4} ${SERVER_USERNAME} ${SERVER_PROJECT_LOCATION}
delete_zip_file
build ${SERVER_IP4} ${SERVER_USERNAME} ${SERVER_PROJECT_LOCATION}
run ${SERVER_IP4} ${SERVER_USERNAME} ${SERVER_PROJECT_LOCATION}
