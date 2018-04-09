run.py

.. image:: https://badge.fury.io/py/run.py.svg
    :target: https://pypi.org/project/runner.py/

.. image:: https://travis-ci.org/mariocesar/run.py.svg?branch=master
    :target: https://travis-ci.org/mariocesar/run.py

Install and Use
---------------

Install with pip.

.. code-block:: console

    pip install runner.py

A simple example on how to use it.

.. code-block:: python

    import asyncio

    from runnerpy.runner import Runner

    if __name__ == '__main__':
        loop = asyncio.get_event_loop()

        runner = Runner(loop)
        runner.run('python manage.py runserver')
        runner.run('celery -A project worker -l INFO')

        runner.start()

Now a Django app will run along the celery worker. Hit ctrl+c to stop both.

Some examples: Creating a backup

.. code-block:: python
    import asyncio

    from runnerpy.runner import Runner

    if __name__ == '__main__':
        loop = asyncio.get_event_loop()

        runner = Runner(loop)
        runner.run('cp -ar dist/static public/static')
        runner.run('pg_dump --all')

        runner.start()

Some examples: Creating a backup

.. code-block:: python
    import asyncio

    from runnerpy.runner import Runner

    if __name__ == '__main__':
        loop = asyncio.get_event_loop()

        runner = Runner(loop)
        runner.run('tail -f /var/log/syslog)
        runner.run('ls -al /home')

        runner.start()
