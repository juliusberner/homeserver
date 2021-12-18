FROM ubuntu AS base
WORKDIR /app
COPY pass_from_env.py .
ENV ANSIBLE_VAULT_PASSWORD_FILE=/app/pass_from_env.py
# see https://github.com/phusion/baseimage-docker/issues/58#issuecomment-47995343
RUN echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections && \
    DEBIAN_FRONTEND=noninteractive apt-get update && \
    apt-get install -y python3-pip python-yaml python-jinja2 && \
    pip install --upgrade pip && \
    pip install ansible jmespath && \
    chmod -R uog=rwx .

FROM base AS ansible-vault
# ansible stores files in ~/.ansible
ENV HOME=/app
ENTRYPOINT ["ansible-vault"]

FROM base AS ansible-playbook
RUN apt-get install -y openssh-client sshpass
ENTRYPOINT ["ansible-playbook"]

FROM base AS local-ansible-playbook
COPY entrypoint.sh .
RUN apt-get install -y ufw sudo cron openssh-server && \
    chmod uog=rx entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]
