#!/bin/sh

docker run -d --privileged --name openvpn-docker -p 1194:1194/udp -p 443:443/tcp beeworking/dockvpn
docker run -d -p 8080:8080 --name serve-config --volumes-from openvpn-docker beeworking/dockvpn serveconfig
