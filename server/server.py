import os
from datetime import date
import tornado.ioloop
import tornado.web
import requests
import os

settings = {'debug': True}


class VersionHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    def get(self):
        response = {'version': '5.5.1',
                    'last_build': date.today().isoformat()}
        self.write(response)


class CovidInfoHandler(tornado.web.RequestHandler):
    country_mapping = {}

    def data_received(self, chunk):
        pass

    #country code 2letters example Ukraine - UA
    def get(self, countryCode):

        country_summary = requests.get('https://api.covid19api.com/summary').json()
        by_countries = country_summary['Countries']
        for country_info in by_countries:
            if country_info['CountryCode'] == countryCode:
                info = "Country: {} TotalDeaths: {} NewConfirmed: {} TotalConfirmed: {}".format(country_info['Country'],
                                                                                                     country_info['TotalDeaths'],
                                                                                                     country_info['NewConfirmed'],
                                                                                                     country_info['TotalConfirmed'])
                self.country_mapping[countryCode] = info
                cmd = "/home/pi/Desktop/display {}".format(info)
                os.system(cmd)
        self.write(self.country_mapping)


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
    (r"/version", VersionHandler),
    (r"/covid/(.*)", CovidInfoHandler)
], settings)

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
