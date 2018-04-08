import asyncio
import os
import sys

from .colors import Color
from .procs import Process

os.setpgrp()


class Runner:
    def __init__(self, ):
        self.loop = asyncio.get_event_loop()
        self.queue = asyncio.Queue()
        self.tasks = []
        self.future = None

    def attach(self, command):
        process = Process(cmd=command, runner=self)
        self.tasks.append(process)

    def start(self):
        asyncio.ensure_future(asyncio.wait([self.loop.create_task(task()) for task in self.tasks]))

        try:
            self.loop.run_forever()
        except KeyboardInterrupt:
            sys.stdout.write('\n')
            sys.stdout.write(Color.fmt('{bold_red}==> Ctrl+C pressed{reset}\n'))
        finally:
            sys.stdout.write(Color.fmt('{bold_red}==> Stopping services{reset}\n'))

            self.loop.run_until_complete(self.stop())
            self.loop.stop()
            self.loop.close()

    async def stop(self):
        await asyncio.wait([task.stop() for task in self.tasks])
        sys.stdout.write(Color.fmt('{bold_red}==> Bye!{reset}\n'))
