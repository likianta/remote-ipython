"""
implemented with pyzmq.
"""
import zmq
import time


def mainloop(userns: dict, port: int) -> None:
    ctx = zmq.Context()
    socket = ctx.socket(zmq.REP)
    socket.bind(f'tcp://0.0.0.0:{port}')
    
    users = {}
    
    while True:
        msg = socket.recv_unicode()
        userid, cmd = msg.split(':', 1)
        if userid not in users:
            users[userid] = userns
        result = eval()
