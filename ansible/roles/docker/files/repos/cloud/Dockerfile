FROM nextcloud

ARG CONFIG_DIR=/usr/src/nextcloud/config

# additional custom config
# mounting the file to the `config` directory prevents the default configs to be copied during the entrypoint
# see https://github.com/nextcloud/docker/blob/3fd3a40ee11a632c815f95d1e45e355b094d0407/docker-entrypoint.sh#L107
COPY custom.config.php $CONFIG_DIR
RUN chmod ug=rw,o=r $CONFIG_DIR/custom.config.php
