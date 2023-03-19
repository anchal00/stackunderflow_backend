FROM python:3.6.9-slim-stretch

RUN ["apt", "update", "-y"]
RUN ["apt", "upgrade", "-y"]
RUN ["apt", "-y", "update"]
RUN ["apt", "install", "libpq-dev" ,"-y"]
RUN ["apt-get", "install", "gcc", "-y"]

COPY . /stackunderflow_backend
WORKDIR /stackunderflow_backend

RUN ["pip", "install", "-r", "requirements.txt"]
RUN chmod +x docker-entrypoint.sh

ENTRYPOINT [ "./docker-entrypoint.sh"]
