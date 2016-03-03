#coding: utf-8
from handlers.index import MainHandler
from handlers.longpolling import LongPollingHandler
from handlers.websocket import WsocketHandler

urls = [
  (r'/', MainHandler),
  (r'/longpolling', LongPollingHandler),
  (r'/ws', WsocketHandler)
]

