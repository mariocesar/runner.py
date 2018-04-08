import asyncio
import os
import signal
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
        self.tasks.append(Process(cmd=command, runner=self))

    def start(self):
        os.setpgrp()
        asyncio.ensure_future(asyncio.wait([self.loop.create_task(task()) for task in self.tasks]))

        try:
            self.loop.run_forever()
        except KeyboardInterrupt:
            sys.stdout.write(Color.fmt('{bold_red}==> Ctrl+C pressed{reset}\n'))
        finally:
            sys.stdout.write(Color.fmt('{bold_red}==> Stopping services{reset}\n'))
            runner.stop()
            os.killpg(0, signal.SIGTERM)

    def stop(self):
        self.loop.stop()
        self.loop.close()


if __name__ == '__main__':
    runner = Runner()

    runner.attach('ls -al')
    runner.attach('ls -al /')
    runner.attach('echo Hello')
    runner.attach('tail -f /var/log/syslog')
    runner.attach('tail -f /var/log/auth.log')
    runner.attach('tail -f /var/log/app/history.log')

    runner.start()
