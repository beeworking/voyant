#!/bin/sh

docker run -d --privileged --name openvpn-docker -e VOYANT_ROOT_URL=$VOYANT_ROOT_URL -e VOYANT_VPN_API_KEY=$VOYANT_VPN_API_KEY -e VOYANT_VPN_PROVIDER=$VOYANT_VPN_PROVIDER -p 1194:1194/udp -p 443:443/tcp vayan/dockvpn
docker run -d -p 8080:8080 --name serve-config --volumes-from openvpn-docker vayan/dockvpn serveconfig
