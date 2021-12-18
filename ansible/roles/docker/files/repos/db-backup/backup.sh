#!/bin/bash
# see https://github.com/fradelg/docker-mysql-cron-backup
BACKUPDIR="backup"
[ -z "${MYSQL_PORT}" ] && { MYSQL_PORT=3306; }

# backup
echo "Backup of $MYSQL_DATABASE at $MYSQL_HOST:$MYSQL_PORT started."
FILENAME="$BACKUPDIR/tmp-$MYSQL_DATABASE.sql"

if mysqldump -h "$MYSQL_HOST" -P "$MYSQL_PORT" -u "$MYSQL_USER" \
  -p"$MYSQL_PASSWORD" "$MYSQL_DATABASE" "$MYSQLDUMP_OPTS" > "$FILENAME"
then
  gzip "-$GZIP_LEVEL" -f "$FILENAME"

  # delete old backups
  echo "Delete old backups..."
  find $BACKUPDIR -name $MYSQL_DATABASE*.sql.gz -mtime +$REMOVE -delete -print
  mv "$FILENAME.gz" "$BACKUPDIR/$MYSQL_DATABASE$(date +-%Y-%m-%d).sql.gz"
  echo "Backup of $MYSQL_DATABASE at $MYSQL_HOST:$MYSQL_PORT finished."

else
  rm -rf "$FILENAME"
  echo "Backup of $MYSQL_DATABASE at $MYSQL_HOST:$MYSQL_PORT failed."
fi
