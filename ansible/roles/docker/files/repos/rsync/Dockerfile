FROM alpine

WORKDIR /app
COPY script.sh .

RUN apk add --no-cache rsync && \
    chmod u=rwx,go=rx script.sh

ENV BACKUPSOURCE=data/
ENV BACKUPDIR=backup

CMD ["sh", "script.sh"]
