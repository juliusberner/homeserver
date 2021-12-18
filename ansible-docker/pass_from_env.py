#!/usr/bin/python3
import os
import sys

ENV_KEY = "ANSIBLE_VAULT_PASSWORD"


def main():
    if not os.environ.get(ENV_KEY):
        sys.stderr.write(f"Environment variable {ENV_KEY} empty or not set.\n")
        sys.exit(1)

    sys.stdout.write(f"{os.environ[ENV_KEY]}\n")
    sys.exit(0)


if __name__ == '__main__':
    main()
