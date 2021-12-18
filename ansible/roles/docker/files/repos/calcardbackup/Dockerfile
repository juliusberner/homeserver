# see https://github.com/waja/docker-calcardbackup
FROM alpine

ENV GIT_PROJECT=BernieO/calcardbackup

WORKDIR /app

RUN apk --no-cache add bash curl findutils mysql-client
RUN apk --no-cache add --virtual build-dependencies tar jq && \
    curl -L "$(curl -s https://codeberg.org/api/v1/repos/$GIT_PROJECT/releases | jq -r ".[0].tarball_url")" | tar xz --strip=1 && \
    # deletes all dependencies of the virtual package named "build-dependencies"
    apk del build-dependencies && \
    chmod u=rwx,go=rx calcardbackup

ENTRYPOINT ["./calcardbackup"]
