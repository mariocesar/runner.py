import asyncio

from runnerpy.runner import Runner

if __name__ == '__main__':
    loop = asyncio.get_event_loop()

    runner = Runner(loop)
    runner.run('./my-script.sh')
    runner.run('./my-script.sh')
    runner.run('./my-script.sh')
    runner.run('./my-script.sh')

    runner.start()
