import IPython
import jupyter_console
import lk_logger
import os
import signal
import sys
import typing as t
from functools import partial
from ipykernel.kernelapp import IPKernelApp
from textwrap import dedent
from threading import Thread
from threading import current_thread
from threading import main_thread

lk_logger.setup(quiet=True, show_source=False)
lk_logger.deflector.add(IPython, lk_logger.bprint, scope=True)
lk_logger.deflector.add(jupyter_console, lk_logger.bprint, scope=True)


def run_server(
    user_ns: dict = None, subthread: bool = False
) -> t.Optional[Thread]:
    if subthread:
        th = Thread(
            # name='remote_ipython_thread',
            target=_run,
            args=(user_ns or {},),
            daemon=True
        )
        th.start()
        return th
    else:
        _run(user_ns or {})


def _run(user_ns: dict) -> None:
    """
    https://stackoverflow.com/questions/11019440/
    """
    pid = os.getpid()
    print(':r', dedent(
        '''
        - To connect to this kernel app, use: [u]python -m remote_ipython -
            run-client [yellow]{}[/][/]
        - To disconnect client from server (which keeps server alive), press -
            [blue]Ctrl+D[/] in client side.
        - To exit, you can press [magenta]Ctrl+C[/] on server side, or send -
            [magenta]quit[/] or [magenta]exit[/] from client side (suggested).
        '''.format(pid)
    ).replace(' -\n    ', ' '))
    
    app = IPKernelApp.instance()
    if current_thread() is main_thread():
        app.init_signal = partial(_init_signal, app.init_signal)
    else:
        # workaround: since signals can only work in main thread, we mask this -
        # method to avoid warning from `app.initialize()`.
        app.init_signal = _skip_init_signal
    app.initialize()
    app.user_ns = user_ns or {}
    app.start()  # blocking
    # print(':v7', 'kernel exit')


def _init_signal(_backup_method: t.Callable) -> None:
    if sys.platform == 'win32':
        # fix `ctrl+c` to correctly kill process on windows.
        # https://stackoverflow.com/a/37420223/9695911
        signal.signal(signal.SIGINT, signal.SIG_DFL)
    else:
        _backup_method()


def _skip_init_signal() -> None:
    pass  # do nothing here


if __name__ == '__main__':
    run_server({'a': 'alpha', 'b': 'beta'})
