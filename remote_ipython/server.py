"""
reference:
    https://github.com/likianta/brilliant-ui/blob/master/brilliant/application -
        /debug.py
    https://github.com/albertz/background-zmq-ipython/blob/master/kernel.py
"""

if 1:
    import os
    # import sys
    import typing as t
    from contextlib import contextmanager
    from os import getpid
    
    import lk_logger
    # from lk_utils import load
    from lk_utils import new_thread

if 2:  # import ipykernal related stuff
    # ignore some warning from ipython kernel.
    os.environ['PYDEVD_DISABLE_FILE_VALIDATION'] = '1'
    
    
    @contextmanager
    def _suppress_kernel_warning() -> t.Iterator:
        with lk_logger.mute():  # TEST: comment this to see what info is buried.
            yield
    
    
    with _suppress_kernel_warning():
        # from IPython import embed_kernel
        from IPython.core.autocall import ZMQExitAutocall
        from ipykernel.embed import embed_kernel
        from ipykernel.kernelapp import IPKernelApp
        from ipykernel.zmqshell import ZMQInteractiveShell


class KernelWrapper:
    _callback: t.Optional[t.Callable]
    _pid: str
    
    def __init__(self, callback: t.Callable = None) -> None:
        self._callback = callback
    
    @property
    def app(self) -> IPKernelApp:
        return IPKernelApp.instance()
    
    @property
    def kernel_id(self) -> str:
        return self._pid
    
    def start(self, user_ns: dict) -> None:
        self._pid = str(getpid())
        print(
            '\nto connect to this kernel, use:\n'
            '    [u][cyan]python -m [yellow]remote_ipython[/] connect-debugger '
            '[cyan]{}[/][/][/]'.format(self._pid),
            ':rs1',
        )
        
        # # https://stackoverflow.com/questions/35094744/where-is-kernel-1234
        # # -json-located-in-jupyter-under-windows
        # if sys.platform == 'win32':
        #     kernel_file = '{}/AppData/Roaming/jupyter/runtime/kernel-{}.json' \
        #         .format(os.environ['USERPROFILE'], self._pid)
        # else:
        #     raise NotImplementedError
        # # https://stackoverflow.com/a/15268945/9695911
        # info = load(kernel_file)
        
        # blocking
        with _suppress_kernel_warning():
            """
            suppress warning from `IPKernelApp.init_signal`, because we do \
            want to do this in a subthread.
            """
            embed_kernel(local_ns=user_ns)
        
        # after
        print(':r', '[red dim]kernel exited[/]')
        if self._callback:
            self._callback()
    
    @new_thread()
    def start_new_thread(self, user_ns: dict) -> None:
        self.start(user_ns)
    
    def close(self) -> None:
        self.app.close()


def run_server(
    user_ns: dict = None, callback: t.Callable = None, new_thread: bool = False
) -> KernelWrapper:
    def _leave() -> None:
        sh = ZMQInteractiveShell.instance()
        exiter = ZMQExitAutocall(ip=sh)
        exiter(keep_kernel=True)
    
    kernel = KernelWrapper(callback=callback)
    user_ns = {
        'leave' : _leave,
        'print' : lk_logger.bprint,
        **(user_ns or {}),
    }
    if new_thread:
        kernel.start_new_thread(user_ns)
        from time import sleep
        sleep(2)
    else:
        kernel.start(user_ns)
    return kernel
