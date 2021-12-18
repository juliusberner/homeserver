#!/bin/bash
# see https://github.com/pschiffe/docker-borg
# and https://github.com/shiz0/borgbackup-docker-alpine
set -euo pipefail

# check passphrase
if [ -z "${BORG_PASSPHRASE:-}" ]; then
  INIT_ENCRYPTION='--encryption=none'
  echo 'No encryption. Set $BORG_PASSPHRASE to encrypt/decrypt your files.'
else
  INIT_ENCRYPTION='--encryption=repokey'
fi

# init borg
if [ ! "$(ls -A $BORG_REPO)" ]; then
  borg init -v --show-rc $INIT_ENCRYPTION
fi

if [ -n "${BORG_CUSTOM_CMD:-}" ]; then
  # custom command (e.g. extract or list)
  borg $BORG_CUSTOM_CMD
else
  # create backup
  cd $BACKUP_DIR
  borg create -v --stats --show-rc --exclude borgbackup \
    $BORG_CREATE_OPTIONS ::"$(date +%Y-%m-%d)" .
fi

# prune
if [ -n "${BORG_PRUNE_OPTIONS:-}" ]; then
  borg prune -v --stats --show-rc --list $BORG_PRUNE_OPTIONS
fi

# check
if [ "${BORG_SKIP_CHECK:-}" != "true" ]; then
  borg check -v --show-rc
fi
