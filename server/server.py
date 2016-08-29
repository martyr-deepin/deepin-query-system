#!/usr/bin/python3

from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

import main

if __name__ == '__main__':
    http_server = HTTPServer(WSGIContainer(main.app))
    http_server.listen(16000)
    IOLoop.instance().start()
