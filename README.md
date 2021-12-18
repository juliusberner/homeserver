# Dockerized Home-Server with Ansible
> [Ansible](https://github.com/ansible/ansible) playbook for configuring a 
> [dockerized](https://github.com/docker/compose) home-server running 
> [nextcloud](https://github.com/nextcloud/docker), 
> [photoprism](https://github.com/photoprism/photoprism), 
> [borgbackup](https://github.com/borgbackup),
> [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot),
> [nginx-proxy](https://github.com/nginx-proxy/nginx-proxy),
> [acme-companion](https://github.com/nginx-proxy/acme-companion),
> [binance-trade-bot](https://github.com/edeng23/binance-trade-bot/blob/master/binance_trade_bot/api_server.py),
> [watchtower](https://github.com/containrrr/watchtower),
> [offlineimap](https://github.com/OfflineIMAP/offlineimap),
> [calcardbackup](https://codeberg.org/BernieO/calcardbackup), and other utilities.

![Project image](project.png)

## Overview
> **This is just a fun project to launch a home-server on an old ThinkPad running Ubuntu Focal Fossa. It should only be used as an inspiration.**

The home-server is configured using Ansible and runs (almost) everything using 
[docker-compose](https://github.com/docker/compose).

The Jinja template for the docker-compose file can be found in 
[`ansible/roles/docker/templates/docker-compose.yml.j2`](ansible/roles/docker/templates/docker-compose.yml.j2).

The home-server features:
- nextcloud with mariadb and redis
- photoprism with mariadb
- nginx proxy with acme companion
- server status using python-telegram-bot
- binance trading bot with api[^*]
- automatic backups (borgbackup, rsync, mysqldump, offlineimap, calcardbackup, lftp)
- automatic updates (watchtower, Ubuntu livepatch, pulling and pruning of docker images)
- DDNS updater
- scheduled suspend and wake using rtcwake

[^*]: While you most likely won't get rich doing this, it serves as a good baseline that can be improved by, 
e.g., adding sentiment analysis of news feeds and time series forecasting.

## Ansible roles

1. **Post-install configuration:** The role in [`ansible/roles/common`](ansible/roles/common) 
sets up basic packages, Ubuntu Livepatch, the admin user, SSH, UFW, TLP, systemd, cron, and rtcwake.

2. **Docker-Compose:** The role in [`ansible/roles/docker`](ansible/roles/docker) 
creates the docker user, installs docker and docker-compose, prepares the docker repos, networks, mounts, cronjobs, and the systemd service.
Then it starts and configures the docker-compose services.

## How-To

If docker-compose is installed on the controller, one can use the 
[`docker-compose.yml`](docker-compose.yml) 
specification to set up the home-server as follows:

1. Create `ansible/hosts.yml` and `ansible/group_vars/all/vault.yml` based on
[`ansible/hosts.example.yml`](ansible/hosts.example.yml)
and 
[`ansible/group_vars/all/vault.example.yml`](ansible/group_vars/all/vault.example.yml).
2. Choose a password and encrypt these files:
`ANSIBLE_VAULT_PASSWORD=ansible_vault_password DOCKER_UID=$(id -g) DOCKER_GID=$(id -u) docker-compose up vault-encrypt`
3. Set up the home-server: `ANSIBLE_VAULT_PASSWORD=ansible_vault_password docker-compose up ansible-install`

Otherwise, one can also install ansible in a virtual environment and directly start the playbook 
[`ansible/site.yml`](ansible/site.yml).
