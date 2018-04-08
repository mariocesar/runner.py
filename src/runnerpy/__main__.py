from runnerpy.runner import Runner

runner = Runner()

runner.attach('ls -al /')
runner.attach('echo Hello World')
runner.attach('dmesg -w')
runner.attach('lsof')
runner.attach('tail -f /var/log/syslog')
runner.attach('tail -f /var/log/auth.log')

runner.start()
