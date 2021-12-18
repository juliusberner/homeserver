#!/bin/bash
# space-separated strings to arrays
# see https://stackoverflow.com/questions/9293887/reading-a-delimited-string-into-an-array-in-bash/53369525
IFS=" " read -ra USERNAME_ARR <<< "$DDNS_USERS"
IFS=" " read -ra PASSWORD_ARR <<< "$DDNS_PASSWORDS"
IFS=" " read -ra DOMAIN_ARR <<< "$DDNS_DOMAINS"

# update
echo "Started DDNS update to: $DDNS_SERVER"
for key in ${!USERNAME_ARR[@]}; do
  RESPONSE=$(curl -s -k -u "${USERNAME_ARR[$key]}:${PASSWORD_ARR[$key]}" \
    --user-agent $DDNS_USER_AGENT $DDNS_SERVER)
  echo "${DOMAIN_ARR[$key]}: $RESPONSE"
done
echo "Finished DDNS update to: $DDNS_SERVER"
