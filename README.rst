Redis Installer
===============

This is a shim package that, that allows you to install [redis](https://redis.io) and the redis
[rejson](http://rejson.io) module using pip!  It also provides API functions to start/stop redis and to check if its
running.

Install with::

    pip3 install [--user] https://github.com/anandtrex/redis-installer/archive/master.zip

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

    # Specify the port where redis should be started (started on port 12345 here)
    start_redis(data_directory='/path/to/data/directory', port=12345)

    # Start redis on a random port, and return the port where its started
    port = start_redis(data_directory='/path/to/data/directory', port='random')

    # Use this to provide your own redis configuration file. The port number in the config file is ignored and redis is
    #^ started on 65535. Pass in the port argument to specify a custom port.
    start_redis(data_directory='/path/to/data/directory', config_file_path='path/to/redis.conf')

    # Stop redis. Without arguments, it will work only if you run from the same host from which it was started.
    stop_redis()

    # Stop redis. You need to pass in the port where it was started if its not on the default port
    stop_redis(port=12345)
    stop_redis(port=port)

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
