#!/usr/bin/env python 

import json
import oauth.oauth as oauth
import os
import requests
import sys
import time
import threading

"""TelldusLive exporter for Prometheus (http://prometheus.io)"""

from BaseHTTPServer import BaseHTTPRequestHandler
from BaseHTTPServer import HTTPServer

from pprint import pprint
from prometheus_client import start_http_server, Gauge, Counter, MetricsHandler

API_URL="https://api.telldus.com"

telldus_sensor_temperature = Gauge('telldus_sensor_temperature', 'Sensor data', ['id', 'name', 'location'])
telldus_sensor_humidity = Gauge('telldus_sensor_humidity', 'Sensor data', ['id', 'name', 'location'])
telldus_sensor_power_kwh_total = Gauge('telldus_sensor_power_kwh_total', 'Sensor data', ['id', 'name', 'location'])
telldus_sensor_power_watt = Gauge('telldus_sensor_power_watt', 'Sensor data', ['id', 'name', 'location']) 
telldus_sensor_power_volt = Gauge('telldus_sensor_power_volt', 'Sensor data', ['id', 'name', 'location']) 
telldus_sensor_power_amp = Gauge('telldus_sensor_power_amp', 'Sensor data', ['id', 'name', 'location']) 


class TelldusLive:

    def __init__(self, apikeys):
        self.apikeys = apikeys

    def get(self, method, params=None):
        consumer = oauth.OAuthConsumer(self.apikeys['public_key'], self.apikeys['private_key'])

        token = oauth.OAuthToken(self.apikeys['token'], self.apikeys['token_secret'])

        oauth_request = oauth.OAuthRequest.from_consumer_and_token(
                consumer, token=token, http_method='GET', http_url=API_URL + "/json/" + method, parameters=params)
        oauth_request.sign_request(oauth.OAuthSignatureMethod_HMAC_SHA1(), consumer, token)
        headers = oauth_request.to_header()
        headers['Content-Type'] = 'application/x-www-form-urlencoded'

        response = requests.get('%s/json/%s' % (API_URL, method), headers=headers, params=params)

        if response.status_code != 200:
            raise Exception(response.text)

        return json.loads(response.text)


# Override the metrics handler in prometheus-client with our own.
class TelldusMetricsHandler(MetricsHandler):

    def do_GET(self):
        epoch_time = int(time.time())

        for sensor in telldus.get('sensors/list')['sensor']:
            sensordata = telldus.get('sensor/info', params = { 'id': sensor['id'], 'includeValues': 1, 'includeScale': 1, 'includeUnit': 1 })

            for data in sensordata['data']:
                if "temp" == data['name']:
                    telldus_sensor_temperature.labels(sensor['id'],sensor['name'],sensor['clientName']).set(data['value'])
                if "humidity" == data['name']:
                    telldus_sensor_humidity.labels(sensor['id'],sensor['name'],sensor['clientName']).set(data['value'])
                if "watt" == data['name'] and "kWh" == data['unit']:
                    telldus_sensor_power_kwh_total.labels(sensor['id'],sensor['name'],sensor['clientName']).set(data['value'])
                if "watt" == data['name'] and "W" == data['unit']:
                    telldus_sensor_power_watt.labels(sensor['id'],sensor['name'],sensor['clientName']).set(data['value'])
                if "watt" == data['name'] and "V" == data['unit']:
                    telldus_sensor_power_volt.labels(sensor['id'],sensor['name'],sensor['clientName']).set(data['value'])
                if "watt" == data['name'] and "A" == data['unit']:
                    telldus_sensor_power_amp.labels(sensor['id'],sensor['name'],sensor['clientName']).set(data['value'])

        MetricsHandler.do_GET(self)


with open('/etc/telldus-exporter/apikeys.json') as f:
    apikeys = json.load(f)
telldus = TelldusLive(apikeys)

def start_http_server(port, addr=''):
    """Starts a HTTP server for prometheus metrics as a daemon thread."""
    class TelldusPrometheusMetricsServer(threading.Thread):
        def run(self):
            httpd = HTTPServer((addr, port), TelldusMetricsHandler)
            httpd.serve_forever()
    t = TelldusPrometheusMetricsServer()
    t.daemon = True
    t.start()


def main(argv):
    start_http_server(9191)

    while True:
        time.sleep(60)


if __name__ == '__main__':
    sys.exit(main(sys.argv))

