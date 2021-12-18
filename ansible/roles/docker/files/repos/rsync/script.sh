#!/bin/sh
date=`date "+%Y-%m-%dT%H_%M_%S"`
rsync $RSYNC_OPTIONS --log-file=$BACKUPDIR/rsync.log --link-dest=$BACKUPDIR/latest $BACKUPSOURCE $BACKUPDIR/back-$date
rm -f $BACKUPDIR/latest
ln -s back-$date $BACKUPDIR/latest
