import zmq

def worker(work_num, backend_port):
    context = zmq.Context()
    socket = context.socket(zmq.PULL)
    socket.connect("tcp://127.0.0.1:%d" % backend_port)

    while True:
        message = socket.recv()
        print "Worker #%s got message! %s" % (work_num, message)
        time.sleep(1)


