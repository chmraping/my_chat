import tornado.websocket
import zmq
from tornado.log import app_log

logger = app_log
c = zmq.Context()

class WsocketHandler(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True

    def open(self, uid):
        # print("WebSocket opened")
        logger.info('opened!%s', uid)
        self.uid = uid
        Operations().set_notifier(self.uid, self)

    def on_message(self, message):
        try:
            o_msg = json.loads(message)
            to_uid = o_msg['to_uid']
            content = o_msg['content']
            Operations().talk_to(self.uid, to_uid, content)
        except Exception, e:
            logger.exception(e)
            self.close(500)

    def on_close(self):
        print("WebSocket closed")
