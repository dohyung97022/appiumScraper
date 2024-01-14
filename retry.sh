while :
do
  killall openvpn
  CONFIG="$(find ./external-files/configurations -type f | shuf -n 1)"
  openvpn --config ${CONFIG} --auth-user-pass ./credentials/surfshark_credentials.conf --daemon
  sleep 15
  curl icanhazip.com
  python main.py
done
