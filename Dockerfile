FROM ubuntu:latest

RUN apt-get update && \
    apt-get install -y python-dev python3-pip

RUN mkdir -p /app/
WORKDIR /app/

ADD requirements.txt /app/
RUN pip3 install -r requirements.txt

ADD . /app/

EXPOSE 8000

CMD ["hug", "-f", "/app/server/__init__.py"]
