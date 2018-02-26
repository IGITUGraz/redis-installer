Redis Installer
===============

This is a shim package that, that allows you to install redis and the redis rejson module using pip!
It also provides one api function that can be used to start/stop redis.

Install with::

    pip3 install [--user] https://github.com/anandtrex/redis-installer/archive/v1.0.0.zip

To install from source, use::

    pip install -r requirements.txt && pip install --upgrade [--user] .

This will download, compile and install the latest stable version of redis and some python packages for redis to your
virtual environment if you are using one.  Otherwise, it will install it to your user python path (~/.local).

After installation, you can use the ``rediscontroller`` package like so:

.. code:: python

    from rediscontroller import start_redis, stop_redis
    # Provide path to the data director here while staring redis. This uses the default config (see notes below)
    #^ and starts redis on PORT 65535
    start_redis(data_directory='/path/to/data/directory')

    # Use this to provide your own redis configuration file and use the PORT you specified there for subsequent access.
    start_redis(data_directory='/path/to/data/directory', config_file_path='path/to/redis.conf')

    # Stop redis. Without arguments, it will work only if you run from the same host from which it was started.
    stop_redis()

    # Otherwise, pass in the redis host and port like so
    stop_redis(redis_host='localhost', redis_port=6379)


Notes
+++++

In the default configuration:

* Redis protected mode is turned OFF. DO NOT run from a host exposed to the internet.
* Redis is configured to be in AOF mode (which might be slow).
* rejson module is installed by default.

If you want to change any of this, specify your own config file when starting redis.

Why??
=====

This package is useful if you (or your users) don't have root access to your system, and still want to use redis,
especially from within a python package. This package is a testament to how really really easy it is to compile and
install redis, since it has almost zero dependencies except a semi-recent gcc and some standard libraries.
