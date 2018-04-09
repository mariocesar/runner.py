import asyncio

from runnerpy.runner import Runner

if __name__ == '__main__':
    loop = asyncio.get_event_loop()

    runner = Runner(loop)
    runner.run('ls /')
    runner.run('ls /home/', essential=True)
    runner.run('tail -f /var/log/syslog')

    runner.start()
