import time
import click
import zmq
from zmq.devices.basedevice import ProcessDevice

@click.command()
@click.option('--frontend_port', '-f', default=5559)
@click.option('--backend_port', '-b', default=5560)
def streamer_device(frontend_port, backend_port):
    frontend_address = "tcp://127.0.0.1:%d" % frontend_port
    backend_address = "tcp://127.0.0.1:%d" % frontend_port

    streamerdevice  = ProcessDevice(zmq.STREAMER, zmq.PULL, zmq.PUSH)
    streamerdevice.bind_in(frontend_address)
    streamerdevice.bind_out(backend_address)
    streamerdevice.setsockopt_in(zmq.IDENTITY, 'PULL')
    streamerdevice.setsockopt_out(zmq.IDENTITY, 'PUSH')
    streamerdevice.start()
    click.echo("started streamer on backend: %s, frontend: %s" %(
        backend_address, frontend_address))

if __name__ == '__main__':
    streamer_device()
