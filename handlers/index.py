#coding:utf-8

import json
import tornado.web 
import tornado.gen
import tornadoredis
import zmq
import logging
from tornado.escape import json_encode
from model.entity import Entity



server = zmq.Context().socket(zmq.PUB)
server.bind('tcp://*:9091')


class MainHandler(tornado.web.RequestHandler) :
  def get(self) :
    name = self.get_argument('name', '')
    entity = Entity.get(name)
    self.set_secure_cookie('name', name)
    #self.write(json_encode(entity.__dict__))
    self.render('index.html', entity = entity)

  @tornado.web.asynchronous
  def post(self) :
    name = self.get_secure_cookie('name')
    msg = self.get_argument('msg', '')

    if name == '':
      name = 'Anonymous'

    data=json_encode({'name':name, 'msg':msg})
    #print data
    server.send(data)

    self.write(json_encode({'result':True}))
    self.finish()
