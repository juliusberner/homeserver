FROM alpine

WORKDIR /app
COPY script.sh .

RUN apk add --no-cache bash curl && \
    chmod u=rw,go=r script.sh

CMD ["bash", "script.sh"]
