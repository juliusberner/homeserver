#!/bin/bash
# see https://github.com/fradelg/docker-mysql-cron-backup
[ -z "${MYSQL_PORT}" ] && { MYSQL_PORT=3306; }
set -o pipefail

echo "Restore $MYSQL_DATABASE at $MYSQL_HOST:$MYSQL_PORT from $1"
SQL=$(gunzip -c "$1")

if echo "$SQL" | mysql -h "$MYSQL_HOST" -P "$MYSQL_PORT" -u "$MYSQL_USER" \
  -p"$MYSQL_PASSWORD" "$MYSQL_DATABASE"
then
  echo "Restore of $MYSQL_DATABASE at $MYSQL_HOST:$MYSQL_PORT succeeded."
else
  echo "Restore of $MYSQL_DATABASE at $MYSQL_HOST:$MYSQL_PORT failed."
fi
