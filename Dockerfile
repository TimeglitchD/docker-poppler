FROM python:3-slim
LABEL MAINTAINER="Diana van der Schouw <timeglitchd@gmail.com>"

WORKDIR /data
VOLUME ["/data"]

RUN apt-get update && \
    apt-get install -y poppler-utils inkscape && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN python3 -m pip install pygments flask gunicorn
COPY app.py .
RUN mkdir media

EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", ":5000", "app:app"]
