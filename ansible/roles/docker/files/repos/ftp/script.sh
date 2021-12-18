#!/bin/bash
# backup directory
LOCAL_DIR="backup"
mkdir -p $LOCAL_DIR

# transfer
echo "Started FTP download from: $FTP_HOST/$FTP_REMOTE_DIR"
lftp -u "$FTP_USER","$FTP_PASSWORD" $FTP_HOST<<EOF
set ftp:ssl-force true
set ftp:ssl-protect-data true
set sftp:auto-confirm yes
mirror --use-pget-n=10 $FTP_REMOTE_DIR $LOCAL_DIR;
exit
EOF
echo "Finished FTP download from: $FTP_HOST/$FTP_REMOTE_DIR"
