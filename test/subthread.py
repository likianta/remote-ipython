import remote_ipython

th = remote_ipython.run_server({'a': 'alpha', 'b': 'beta'}, subthread=True)
input('press enter to exit...')
th.close()

# pox test/subthread.py
