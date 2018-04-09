import asyncio
import shlex
import signal
import sys
from asyncio import subprocess
from itertools import chain

from .colors import Color

colors = chain([Color.cyan, Color.magenta, Color.yellow,
                Color.green, Color.light_blue, Color.white,
                Color.grey, Color.light_red, Color.light_green])


class EssentialProcessStoped(Exception):
    def __init__(self, proc):
        self.proc = proc


class SubprocessProtocol(asyncio.SubprocessProtocol):
    def __init__(self, proc):
        self.proc = proc

    def connection_made(self, transport):
        self.transport = transport
        self.proc.log(f'Running {self.proc.cmd} pidfile={transport.get_pid()}', transport)
        sys.stdout.flush()

    def pipe_data_received(self, fd, data):
        out = data.decode().strip().split('\n')

        for line in out:
            self.proc.log(line, self.transport)

        sys.stdout.flush()

    def process_exited(self):
        returncode = self.transport.get_returncode()
        self.proc.returncode.set_result(returncode)


class Process:
    transport = None
    protocol = None

    def __init__(self, cmd, runner, essential=False):
        self.cmd = cmd
        self.essential = essential
        self.prefix = self.cmd.split()[0]
        self.queue = runner.queue
        self.loop = runner.loop
        self.runner = runner
        self.color = next(colors)

        self.returncode = asyncio.Future(loop=self.loop)
        self.returncode.add_done_callback(self.returncode_callback)

    def returncode_callback(self, future):
        self.log(f'Process exited returncode={future.result()}')

    async def __call__(self):
        command = shlex.split(self.cmd)

        process = await self.loop.subprocess_exec(
            lambda: SubprocessProtocol(self),
            *command,
            stdin=None,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)

        self.transport, self.protocol = process
        self.queue.put((self.transport, self.protocol))

        await self.returncode

        if self.essential:
            self.log(f'Essential process has stopped, stopping runner')

            await self.runner.stop(exitcode=1)

    def log(self, line, transport=None):
        if transport is None:
            transport = self.transport

        sys.stdout.write(Color.fmt(
            '{bold}{prefix} {color}pid={pid}{reset} | {reset}{color}{line}{reset}\n',
            color=self.color,
            pid=transport.get_pid() if transport else '',
            prefix=self.prefix,
            line=line))

        sys.stdout.flush()

    async def stop(self):
        self.log(f'Closing {self.cmd} pid={self.transport.get_pid()}')

        try:
            self.transport.send_signal(signal.SIGINT)
        except ProcessLookupError:
            pass

        await self.returncode
