from datetime import date, datetime
import tornado.ioloop
import tornado.web
import requests
import os

from pi import util

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

    # country code 2letters example Ukraine - UA
    def get(self, country_code):
        covid_api_com_summary = 'https://api.covid19api.com/summary'

        try:
            with requests.get(covid_api_com_summary) as summary_response:
                summary = summary_response.json()
        except:
            print("Cant get info, information not updated")
            return

        by_countries = summary['Countries']
        for country_info in by_countries:
            if country_info['CountryCode'] == str(country_code).upper():
                info = "Covid19_DAY State:{} Death:{}+{} New:{} AllCases:{}".format(country_info['Country'],
                                                                                    country_info['TotalDeaths'],
                                                                                    country_info['NewDeaths'],
                                                                                    country_info['NewConfirmed'],
                                                                                    country_info['TotalConfirmed'])
                self.country_mapping[country_code] = info
                util.Dispaly.show(info)
        print("Called at-{} DATA:{}".format(datetime.now(), self.country_mapping))
        self.write(self.country_mapping)


application = tornado.web.Application([
    (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': os.path.join('static')}),
    (r"/version", VersionHandler),
    (r"/covid/(.*)", CovidInfoHandler)
], settings)

if __name__ == "__main__":
    port = 8888
    application.listen(port)
    print("Server started at {}".format(port))
    tornado.ioloop.IOLoop.instance().start()
