import click
from multiprocessing import Process

from photomgr.zmqutils.push_client import worker

@click.command()
@click.option('--backend_port', default=5560)
def run_test(backend_port):
    number_of_workers = 2
    for work_num in range(number_of_workers):
        Process(target=worker, args=(work_num, backend_port,)).start()

if __name__ == '__main__':
    run_test()

