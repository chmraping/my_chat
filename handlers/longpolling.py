import random
import time
import tornado.web
import tornado.gen
import tornadoredis
import zmq
from tornado.escape import json_encode
from model.entity import Entity


class LongPollingHandler(tornado.web.RequestHandler):
    socket = None

    def initialize(self):
        self.socket = zmq.Context().socket(zmq.SUB)
        self.socket.setsockopt(zmq.SUBSCRIBE, '')
        self.socket.connect('tcp://localhost:9091')

    @tornado.web.asynchronous
    def get(self):
        self.get_data()
    @tornado.web.asynchronous
    def post(self):
        self.get_data()

    @tornado.gen.coroutine
    def subscribe(self):
        data =  tornado.gen.Task(self.socket.recv, None)
        print data.
        self.on_message(data)

    @tornado.gen.coroutine
    def recieve(self):
        data = yield tornado.gen.Task(self.socket.recv())
        print data
        self.on_message(data)
        raise tornado.gen.Return()

    def get_data(self):
        if self.request.connection.stream.closed():
            return

        try:
            self.subscribe()
        except Exception, e:
            print e
            pass

        num = 10
        self.time_handler = tornado.ioloop.IOLoop.instance().add_timeout(
            time.time() + num,
            lambda: self.on_timeout(num)
        )


    def on_timeout(self, num):
        self.time_handler = None
        self.send_data(json_encode({'name': '', 'msg': ''}))

    def send_data(self, data):
        if self.request.connection.stream.closed():
            return

        self.set_header('Content-Type', 'application/json; charset=UTF-8')
        self.write(data)
        self.finish()


    def on_message(self, msg):
        if (msg is not None):
            self.send_data(msg)

    #def remove_time_handler(self):
        #if self.time_handler:
            #tornado.ioloop.IOLoop.instance().remove_timeout(self.time_handler)
            #self.time_handler = None

    #def on_finish(self):
        #self.remove_time_handler()
        #if (self.socket.subscribed):
            #self.socket.unsubscribe('test_channel')

    #def on_connection_close(self):
        #self.finish()
