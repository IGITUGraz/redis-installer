Redis Installer
===============

This is a shim package that, that allows you to install redis and the redis rejson module using pip!
It also provides one api function that can be used to start/stop redis.

Run with::

    pip install --upgrade .

This will download, compile and install the latest stable version of redis to the virtual environment, and install all dependencies.

Then use the ``rediscontroller`` package like so:

.. code:: python

    from rediscontroller import start_redis, stop_redis
    # Provide path to the data director here while staring redis. This uses the default config (see warnings below)
    start_redis(data_directory='/path/to/data/directory')

    # Use this to provide your own redis configuration file
    start_redis(data_directory='/path/to/data/directory', config_file_path='path/to/redis.conf')

    # Stop redis. This will work only if run from the same host from which it was started.
    stop_redis()

    # Otherwise, pass in the redis host and port like so
    stop_redis(redis_host='localhost', redis_port=6379)


Warnings
++++++++

* Works only from within a virtual environment.
* Redis protected mode is turned OFF. DO NOT run from a host exposed to the internet.
* Redis is configured to be in AOF mode (which might be slow).
* rejson module is installed by default.
