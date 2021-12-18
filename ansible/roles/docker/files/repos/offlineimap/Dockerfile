FROM ubuntu

WORKDIR /app
COPY credentials_from_env.py .
COPY .offlineimaprc /.offlineimaprc

RUN apt-get update && \
    apt-get install -y offlineimap ca-certificates && \
    chmod u=rwx,go=rx credentials_from_env.py /.offlineimaprc

CMD ["offlineimap", "-u", "Noninteractive.Basic"]
