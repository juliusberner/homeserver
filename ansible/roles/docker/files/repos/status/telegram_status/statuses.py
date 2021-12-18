from datetime import datetime
import logging
import os
from pathlib import Path
import pytz

import requests
from socket import gethostbyname


TIMEZONE = pytz.timezone(os.environ.get("TZ", "UTC"))
LOG_PATH = Path("/app/data")
IP_SERVICE = "https://api.ipify.org"
TIMEOUT = 2

logging.basicConfig(format="%(name)s %(levelname)s %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)


def timestamp(time=None):
    if time is None:
        time = datetime.now(TIMEZONE)
    return f"{time:%Y-%m-%d %H:%M}"


def domains_status():
    result = {}
    for domain in os.environ["DOMAINS"].split(" "):
        for protocol in ["http://", "https://"]:
            addr = f"{protocol}{domain}"
            try:
                status_code = requests.get(addr, timeout=TIMEOUT).status_code
                result[addr] = dict(
                    msg=f"status-code: {status_code}",
                    error=status_code != 200,
                    time=timestamp(),
                )

            except requests.exceptions.RequestException as err:
                result[addr] = dict(
                    msg="connection error", error=True, time=timestamp()
                )
                logger.error(f"{addr} connection error.", exc_info=err)
    return result


def ddns_status():
    result = {}
    try:
        public_ip = requests.get(IP_SERVICE, timeout=TIMEOUT).content.decode("utf8")
        result[IP_SERVICE] = dict(
            msg=f"public IP: {public_ip}", error=False, time=timestamp()
        )

        for domain in os.environ["DDNS_DOMAINS"].split(" "):
            try:
                points_to = gethostbyname(domain)
                result[domain] = dict(
                    msg=f"points to: {points_to} public IP: {public_ip}",
                    error=public_ip != points_to,
                    time=timestamp(),
                )
            except OSError as err:
                result[domain] = dict(msg="address error", error=True, time=timestamp())
                logger.error(f"{domain} address error.", exc_info=err)

    except requests.exceptions.RequestException as err:
        result[IP_SERVICE] = dict(msg="connection error", error=True, time=timestamp())
        logger.error(f"{IP_SERVICE} connection error.", exc_info=err)

    return result


def docker_status():
    result = {}
    path = LOG_PATH / "docker-ps.txt"
    if path.is_file():
        ps_timestamp = timestamp(datetime.fromtimestamp(path.stat().st_mtime))
        with path.open(mode="r") as f:
            lines = f.read().splitlines()

        for line in lines[1:]:
            substr = line.split()
            try:
                error = substr[1] != "Up" and substr[2] != "(0)"
            except IndexError:
                error = True
            result[substr[0]] = dict(
                msg=" ".join(substr[1:]), error=error, time=ps_timestamp
            )

    return result
