from runnerpy.runner import Runner

runner = Runner()

runner.attach('ls -al')
runner.attach('ls -al /')
runner.attach('echo Hello')
runner.attach('tail -f /var/log/syslog')
runner.attach('tail -f /var/log/auth.log')
runner.attach('tail -f /var/log/app/history.log')

runner.start()
