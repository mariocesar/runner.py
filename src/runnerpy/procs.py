import asyncio
import shlex
import sys
from asyncio import subprocess
from itertools import chain

from .colors import Color

colors = chain([Color.cyan, Color.magenta, Color.yellow, Color.green, Color.light_blue, Color.white])


class SubprocessProtocol(asyncio.SubprocessProtocol):
    def __init__(self, future, prefix, color):
        self.color = color
        self.future = future
        self.prefix = prefix

    def pipe_data_received(self, fd, data):
        out = data.decode().strip().split('\n')
        for line in out:
            sys.stdout.write(Color.fmt('{bold}{proc.prefix} | {reset}{proc.color}{line}{reset}\n',
                                       proc=self,
                                       line=line))
        sys.stdout.flush()

    def pipe_connection_lost(self, fd, exc):
        self.future.set_exception(exc)

    def connection_lost(self, exc):
        self.future.set_exception(exc)

    def process_exited(self):
        self.future.set_result(True)


class Process:
    def __init__(self, cmd, runner):
        self.cmd = cmd
        self.prefix = self.cmd.split()[0]
        self.queue = runner.queue
        self.loop = runner.loop

    async def __call__(self):
        future = asyncio.Future(loop=self.loop)
        color = next(colors)

        sys.stdout.write(f'{Color.bold}{self.prefix} => {color}{self.cmd}{Color.reset}\n')
        sys.stdout.flush()

        process = await self.loop.subprocess_exec(
            lambda: SubprocessProtocol(future, self.prefix, color),
            *shlex.split(self.cmd),
            stdin=None,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)

        pipe, protocol = process

        self.queue.put((pipe, protocol))

        await future
        pipe.close()
        return protocol.output
