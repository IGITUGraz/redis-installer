import os
from contextlib import contextmanager, closing

from socket import socket, SOL_SOCKET, SO_REUSEADDR
from socket import error as SocketError


@contextmanager
def changed_dir(dirname):
    try:
        cwd = os.getcwd()
        os.chdir(dirname)
        yield
    finally:
        os.chdir(cwd)


def which(program):
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return None


def get_install_prefix():
    install_prefix = os.environ.get('VIRTUAL_ENV')
    if install_prefix is None:
        print("Looking for config in user home ~/.local")
        install_prefix = os.path.expanduser('~/.local')
    return install_prefix

# The function below, is taken from
#
# https://github.com/Yelp/ephemeral-port-reserve/blob/master/ephemeral_port_reserve.py
#
# It is provided under the MIT license
#
# The MIT License (MIT)
#
# Copyright (c) 2016 Yelp
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.


def reserve_port(port, ip='localhost'):
    """Bind to an ephemeral port, force it into the TIME_WAIT state, and unbind it.
    This means that further ephemeral port alloctions won't pick this "reserved" port,
    but subprocesses can still bind to it explicitly, given that they use SO_REUSEADDR.
    By default on linux you have a grace period of 60 seconds to reuse this port.
    To check your own particular value:
    $ cat /proc/sys/net/ipv4/tcp_fin_timeout
    60
    By default, the port will be reserved for localhost (aka 127.0.0.1).
    To reserve a port for a different ip, provide the ip as the first argument.
    Note that IP 0.0.0.0 is interpreted as localhost.

    """
    port = int(port)
    with closing(socket()) as s:
        s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        try:
            s.bind((ip, port))
        except SocketError as e:
            # socket.error: [Errno 98] Address already in use
            if e.errno == 98:
                return None
            else:
                raise

        # the connect below deadlocks on kernel >= 4.4.0 unless this arg is greater than zero
        s.listen(1)

        sockname = s.getsockname()

        # these three are necessary just to get the port into a TIME_WAIT state
        with closing(socket()) as s2:
            s2.connect(sockname)
            s.accept()
            return sockname[1]
