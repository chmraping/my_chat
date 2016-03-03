import zmq
c=zmq.Context()
#s=c.socket(zmq.REQ)
s = c.socket(zmq.SUB)
s.setsockopt(zmq.SUBSCRIBE, '')
s.connect('tcp://localhost:9091')
while True:
    msg = s.recv()
    print(msg)