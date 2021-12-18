#!/bin/bash
if [ ! -f /root/.ssh/id_rsa ]; then
  # create dummy key
  ssh-keygen -t rsa -f /root/.ssh/id_rsa
fi

# see https://github.com/husarnet/docker-example/issues/1
update-alternatives --set ip6tables /usr/sbin/ip6tables-nft

# services do not start using ansible in container
service cron start
service ssh start

exec ansible-playbook -i localhost, -c local "$@"