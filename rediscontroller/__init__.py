import os
from .controller import start_redis, stop_redis, is_redis_running

__all__ = ['start_redis', 'stop_redis', 'is_redis_running']


def which(program):
    import os
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
