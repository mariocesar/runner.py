import asyncio
import shlex
import sys
from asyncio import subprocess
from itertools import chain

from .colors import Color

colors = chain([Color.cyan, Color.magenta, Color.yellow, Color.green, Color.light_blue, Color.white])


class SubprocessProtocol(asyncio.SubprocessProtocol):
    def __init__(self, future, color, proc):
        self.color = color
        self.future = future
        self.prefix = proc.prefix
        self.proc = proc

    def connection_made(self, transport):
        self.transport = transport

        sys.stdout.write(f'{Color.bold}{self.prefix} => {self.color}{self.proc.cmd}{Color.reset}\n')
        sys.stdout.flush()


    def pipe_data_received(self, fd, data):
        out = data.decode().strip().split('\n')
        for line in out:
            sys.stdout.write(Color.fmt('{bold}{proc.prefix} | {reset}{proc.color}{line}{reset}\n',
                                       proc=self,
                                       line=line))
        sys.stdout.flush()

    def process_exited(self):
        returncode = self.transport.get_returncode()
        sys.stdout.write(Color.fmt('{bold}{proc.prefix} | {proc.color}{line}{reset}\n',
                                   proc=self,
                                   line=f'{self.proc.cmd} => Process exited'))

        self.future.set_result(returncode)


class Process:
    def __init__(self, cmd, runner):
        self.cmd = cmd
        self.prefix = self.cmd.split()[0]
        self.queue = runner.queue
        self.loop = runner.loop

    async def __call__(self):
        future = asyncio.Future(loop=self.loop)
        color = next(colors)

        process = await self.loop.subprocess_exec(
            lambda: SubprocessProtocol(future, color, self),
            *shlex.split(self.cmd),
            stdin=None,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)

        transport, protocol = process

        self.queue.put((transport, protocol))

        await future

        transport.close()

        return protocol.output
