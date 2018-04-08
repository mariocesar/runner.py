from runnerpy.runner import Runner

if __name__ == '__main__':
    runner = Runner()

    runner.attach('ls /')
    runner.attach('ls /home/')
    runner.attach('./my-script.sh')

    runner.start()

