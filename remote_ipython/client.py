"""
reference:
    https://github.com/likianta/brilliant-ui/blob/master/brilliant/application -
        /debug.py
    https://github.com/albertz/background-zmq-ipython/blob/master/kernel.py
"""

import lk_logger
from jupyter_console.app import ZMQTerminalIPythonApp
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory


def run_client(kernel_id: str) -> None:
    lk_logger.unload()
    
    instance = ZMQTerminalIPythonApp.instance()
    instance.initialize(
        argv=['console', '--existing', kernel_id],
    )
    # fix no prompt
    # https://blog.csdn.net/Likianta/article/details/131486249
    instance.shell.pt_cli.auto_suggest = AutoSuggestFromHistory()
    instance.start()  # blocking
    
    lk_logger.setup(quiet=True)
