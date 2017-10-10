Redis Installer
===============

This is a shim package that, when installed, downloads and installs the latest stable redis to the same path as the python which is used to run it. It is recommended to only use this from a virtual environment. It also provides one api function that can be used to run redis.

Run with::

    pip install --upgrade .

This will download, compile and install the latest stable version of redis to the virtual environment.

Then use the ``rediscontroller`` package like so:

.. code:: python

    from rediscontroller import start_redis, stop_redis
    # Provide path to the data director here while staring redis
    start_redis('/path/to/data/directory')

    # Stop redis. This will work only if run from the same host from which it was started.
    stop_redis()

    # Otherwise, pass in the redis host and port like so
    stop_redis(redis_host='localhost', redis_port=6379)
