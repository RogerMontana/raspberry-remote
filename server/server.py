import os
from datetime import date
import tornado.ioloop
import tornado.web

settings = {'debug': True}


class VersionHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    def get(self):
        response = {'version': '5.5.1',
                    'last_build': date.today().isoformat()}
        self.write(response)


class ProviderByIdHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    def get(self, id):
        response = {'id': int(id),
                    'name': 'Provider Cafe',
                    'release_date': date.today().isoformat()}
        self.write(response)


application = tornado.web.Application([
    (r"/getProvider/([0-9]+)", ProviderByIdHandler),
    (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': os.path.join('static')}),
    (r"/version", VersionHandler)
], settings)

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
