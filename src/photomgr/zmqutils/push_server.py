import click
import zmq

@click.command()
@click.option('--frontend_port', default=5559)
def server(frontend_port):
    context = zmq.Context()
    socket = context.socket(zmq.PUSH)
    socket.connect("tcp://127.0.0.1:%d" % frontend_port)

    for i in xrange(0,10):
        socket.send('#%s' % i)

if __name__ == '__main__':
    server()
