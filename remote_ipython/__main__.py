from argsense import cli

from .client import run_client
from .server import run_server

cli.add_cmd(run_server)
cli.add_cmd(run_client)

if __name__ == '__main__':
    # pox -m remote_ipython run-server
    # pox -m remote_ipython run-client <kernel_id>
    cli.run()
