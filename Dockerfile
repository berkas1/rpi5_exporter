FROM alpine:3.19.0

RUN apk update && apk add --no-cache \
    python3 raspberrypi-utils-vcgencmd 

WORKDIR /app

COPY exporter.py /app

EXPOSE 8878

ENTRYPOINT ["python3", "exporter.py", "--webserver"]
