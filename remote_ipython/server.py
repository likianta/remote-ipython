import IPython
import jupyter_console
import lk_logger
import os
import typing as t
from ipykernel.kernelapp import IPKernelApp
from textwrap import dedent
from threading import Thread


def run_server(
    user_ns: dict = None, subthread: bool = False
) -> t.Optional[Thread]:
    if subthread:
        th = Thread(target=_run, args=(user_ns or {},), daemon=True)
        th.start()
        return th
    else:
        _run(user_ns or {})


def _run(user_ns: dict) -> None:
    """
    https://stackoverflow.com/questions/11019440/
    """
    lk_logger.setup(quiet=True, show_source=False)
    lk_logger.deflector.add(IPython, lk_logger.bprint, scope=True)
    lk_logger.deflector.add(jupyter_console, lk_logger.bprint, scope=True)
    
    pid = os.getpid()
    print(':r', dedent(
        '''
        - To connect to this kernel app, use:
            [u]python -m remote_ipython run-client [yellow]{}[/][/]
        - To disconnect client from server (which keeps server alive), press
            [blue]Ctrl+D[/] in client side.
        - To exit, you will have to explicitly kill this process, or send
            [magenta]quit[/] or [magenta]exit[/] from client side.
        '''.format(pid)
    ))
    
    app = IPKernelApp.instance()
    app.initialize()
    app.user_ns = user_ns or {}
    app.start()


if __name__ == '__main__':
    run_server({'a': 'alpha', 'b': 'beta'})
