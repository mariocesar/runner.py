import asyncio
import os
import sys

from .colors import Color
from .procs import Process

os.setpgrp()


class Runner:
    def __init__(self, loop):
        self.loop = loop
        self.queue = asyncio.Queue()
        self.tasks = []

    def run(self, command, essential=False):
        process = Process(cmd=command, runner=self, essential=essential)
        self.tasks.append(process)

    async def start_tasks(self):
        await asyncio.ensure_future(asyncio.wait([
            self.loop.create_task(task()) for task in self.tasks
        ]))

    def start(self):
        try:
            self.loop.run_until_complete(self.start_tasks())
        except KeyboardInterrupt:
            print()
            self.loop.run_until_complete(self.stop())
        finally:
            if self.loop.is_running():
                self.loop.close()

    async def stop(self, exitcode=0):
        sys.stdout.write(Color.fmt('{bold_red}==> Stopping!{reset}\n'))

        await asyncio.wait([task.stop() for task in self.tasks if not task.returncode.done()])

        sys.stdout.write(Color.fmt('{bold_red}==> Bye!{reset}\n'))

        self.loop.stop()

        sys.exit(exitcode)
