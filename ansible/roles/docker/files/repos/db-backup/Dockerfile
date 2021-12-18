FROM alpine

WORKDIR /app
COPY backup.sh restore.sh ./

RUN apk add --no-cache bash mysql-client gzip && \
    chmod u=rw,go=r backup.sh restore.sh

CMD ["bash", "backup.sh"]
