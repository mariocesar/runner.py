import asyncio
import os
import shlex
import sys
from asyncio import subprocess
from itertools import chain

RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
BLUE = '\033[34m'
MAGENTA = '\033[35m'
CYAN = '\033[36m'

LIGHT_RED = '\033[91m'
LIGHT_GREEN = '\033[92m'
LIGHT_YELLOW = '\033[93m'
LIGHT_BLUE = '\033[94m'
LIGHT_MAGENTA = '\033[95m'
LIGHT_CYAN = '\033[96m'

WHITE = '\033[97m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'
END = '\033[0m'
RESET = '\033[0m'

# Set up a new process group, so that we can later kill run{server,tornado}
# and all of the processes they spawn.
os.setpgrp()

colors = chain([CYAN, MAGENTA, YELLOW, GREEN, LIGHT_BLUE])
queue = asyncio.Queue()


class SubprocessProtocol(asyncio.SubprocessProtocol):
    def __init__(self, future, prefix, color):
        self.color = color
        self.future = future
        self.prefix = prefix

    def pipe_data_received(self, fd, data):
        out = data.decode().strip().split('\n')
        for line in out:
            sys.stdout.write(f'{BOLD}{self.prefix} | {RESET}{self.color}{line}{RESET}\n')
        sys.stdout.flush()

    def pipe_connection_lost(self, fd, exc):
        self.future.set_exception(exc)

    def connection_lost(self, exc):
        self.future.set_exception(exc)

    def process_exited(self):
        self.future.set_result(True)


futures = {}


async def run(loop, name, cmd):
    prefix = name
    future = futures[prefix] = asyncio.Future(loop=loop)
    color = next(colors)

    process = await loop.subprocess_exec(
        lambda: SubprocessProtocol(future, prefix, color),
        *shlex.split(cmd),
        stdin=None,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)

    pipe, protocol = process

    sys.stdout.write(f'{BOLD}{prefix} => {color}{cmd}{RESET}\n')
    sys.stdout.flush()

    await future
    sys.stdout.write(f'{BOLD}{prefix} => {color} Canceled {RESET}\n')
    pipe.close()


if __name__ == '__main__':
    sys.stdout.write(f'{GREEN}{BOLD}==> Starting services{RESET}\n')

    services = {
        "backend": "python ./src/manage.py runserver --no-color 0.0.0.0:8000",
        "worker": "celery -A modus worker --no-color --concurrency 2  -l INFO",
        "flower": "celery -A modus flower --port=5555",
        "beat": "celery -A modus beat --no-color -l INFO",
        "channel": "python src/manage.py runworker events"
    }

    loop = asyncio.get_event_loop()
    tasks = [loop.create_task(run(loop, name, cmd)) for name, cmd in services.items()]
    asyncio.ensure_future(asyncio.wait(tasks))

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        sys.stdout.write(f'{RED}{BOLD}==> Ctrl+C pressed{RESET}\n')
    finally:
        for future in futures:
            sys.stdout.write(f'{RED}{BOLD}==> Stopping service {future} {RESET}\n')
            futures[future].set_exception(asyncio.CancelledError)

        loop.close()
