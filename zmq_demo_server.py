import zmq
c=zmq.Context()
#s=c.socket(zmq.REP)
s = c.socket(zmq.PUB)
s.bind('tcp://*:9091')

s.send('')
