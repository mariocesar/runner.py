from runnerpy.runner import Runner

if __name__ == '__main__':
    runner = Runner()

    runner.attach('./my-script.sh')
    runner.attach('./my-script.sh')
    runner.attach('./my-script.sh')
    runner.attach('./my-script.sh')

    runner.start()
