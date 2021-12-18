import json
import logging

from . import statuses


STATUS_HANDLER = {
    "docker": statuses.docker_status,
    "domains": statuses.domains_status,
    "ddns": statuses.ddns_status,
}

logging.basicConfig(format="%(name)s %(levelname)s %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)


def update_status(msg_func, context):
    for service_name, service_status_fn in STATUS_HANDLER.items():

        path = statuses.LOG_PATH / f"status-{service_name}.json"

        service = {}
        if path.is_file():
            with path.open(mode="r") as f:
                service = json.load(f)

        for name, new_status in service_status_fn().items():

            old_status = service.get(name, {})

            if not new_status["error"] is old_status.get("error", False):
                if new_status["error"]:
                    msg = f"ERROR [{service_name}] {name} {new_status['msg']}"
                else:
                    msg = f"RECOVERED [{service_name}] {name} {new_status['msg']}"

                logger.info(msg)
                msg_func(text=msg)

            service[name] = new_status

        with path.open(mode="w+") as f:
            json.dump(service, f, indent=2)

        errors = {name: status for name, status in service.items() if status["error"]}
        with (statuses.LOG_PATH / f"error-{service_name}.json").open(mode="w+") as f:
            json.dump(errors, f, indent=2)


def next_update(msg_func, context):
    current_jobs = context.job_queue.get_jobs_by_name("auto_updater")
    if not current_jobs:
        msg_func(text="Updater not running.")
    else:
        msg_func(text=f"Next update: {current_jobs[0].next_t:%Y-%m-%d %H:%M}")


def clear(msg_func, context):
    for f in statuses.LOG_PATH.iterdir():
        f.unlink()
        msg = f"{f.stem} deleted."
        msg_func(text=msg)
        logger.info(msg)
