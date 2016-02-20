#!/bin/sh

CID=$(docker run -d --privileged -p 1194:1194/udp -p 443:443/tcp jpetazzo/dockvpn)

echo
echo "========== Download file from :"
echo

docker run -t -i -p 8080:8080 --volumes-from $CID jpetazzo/dockvpn serveconfig
