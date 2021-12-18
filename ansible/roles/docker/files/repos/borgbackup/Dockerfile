FROM alpine

WORKDIR /app
COPY script.sh .

# TODO: Switch to pyfuse3 https://github.com/borgbackup/borg/issues/5407
# (probably replace fuse-dev by fuse3-dev and llfse by pyfuse3)
RUN apk add --no-cache bash py3-pip fuse-dev borgbackup && \
    chmod u=rw,go=r script.sh

RUN apk --no-cache add --virtual build-dependencies gcc python3-dev musl-dev linux-headers && \
    pip3 install --upgrade pip && \
    pip3 install llfuse && \
    # deletes all dependencies of the virtual package named "build-dependencies"
    apk del build-dependencies && \
    echo "user_allow_other" > /etc/fuse.conf

# borg extracts files to this directory
WORKDIR /app/borgbackup
# see https://borgbackup.readthedocs.io/en/stable/usage/general.html
ENV BORG_BASE_DIR=/app/borgbackup/cache
ENV BORG_REPO=/app/borgbackup/backup
ENV BACKUP_DIR=/app/data

CMD ["bash", "/app/script.sh"]
