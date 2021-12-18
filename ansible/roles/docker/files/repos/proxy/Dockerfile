FROM nginxproxy/nginx-proxy

ARG CONFIG_DIR=/etc/nginx/conf.d

# see https://github.com/nginx-proxy/nginx-proxy#proxy-wide
COPY custom.conf $CONFIG_DIR
RUN chmod u=rw,go=r $CONFIG_DIR/custom.conf
