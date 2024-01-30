FROM ubuntu:jammy
ENV DEBIAN_FRONTEND noninteractive
LABEL MAINTAINER="Diana van der Schouw <timeglitchd@gmail.com>"

WORKDIR /data
VOLUME ["/data"]

RUN apt-get update && \
    apt-get install -y python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools poppler-utils inkscape && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN python3 -m pip install pygments flask gunicorn
COPY app.py .
RUN mkdir media

EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", ":5000", "app:app"]
