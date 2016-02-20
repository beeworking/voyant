FROM ubuntu:latest

RUN apt-get update && \
    apt-get install -y python-dev python3-pip

RUN mkdir -p /app/
WORKDIR /app/

ADD requirements.txt /app/
RUN pip3 install -r requirements.txt

ADD . /app/

EXPOSE 8000

CMD ["gunicorn", "--reload", "-b", "0.0.0.0:8000", "-w", "4", "server:__hug_wsgi__"]
