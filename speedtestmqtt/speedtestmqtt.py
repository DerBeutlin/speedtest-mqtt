# -*- coding: utf-8 -*-
import logging
import paho.mqtt.client as paho
import time
from .speedtestprocess import SpeedTest


def sizeof_fmt(num, suffix='B'):
    """
    Properly format bytes. From
      https://stackoverflow.com/a/1094933/5480526
    """
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f %s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f %s%s" % (num, 'Yi', suffix)


class SpeedTestMQTT(object):
    
    def __init__(self, mqtt_broker, mqtt_client_id="speedtest",
                 mqtt_topic="speedtest", log_level=logging.ERROR):
        super(SpeedTestMQTT, self).__init__()
        self._interval = 3600
        self._mqtt_broker = mqtt_broker
        self._mqtt_client_id = mqtt_client_id
        self._mqtt_topic = mqtt_topic
        self._log_level = log_level
        self._run = False
        self._speedtest = None
        self._logger = logging.getLogger("speedtest-mqtt.MQTT")
        self._logger.setLevel(log_level)
        self._last_run = time.time()
        
    def on_mqtt_recv(self, client, data, msg):
        mqtt_top = msg.topic
        mqtt_msg = msg.payload.decode("utf8")
        self._logger.debug("Received message: {0}.".format(mqtt_msg))
        
        if mqtt_top == self._mqtt_topic + "/command/run" and mqtt_msg == "run":
            self.run_speedtest()
        elif mqtt_top == self._mqtt_topic + "/command/interval":
            self._interval = int(mqtt_msg)
            self._logger.info("Speedtest interval set to {0} s.".format(self._interval))
        
    def run_speedtest(self):
        if self._speedtest is not None:
            return
        self._last_run = time.time()
        self._client.publish(self._mqtt_topic + "/state/running", "1")
        self._logger.info("Speedtest started.")
        self._speedtest = SpeedTest()
        self._speedtest.start()
        
    def on_speedtest_finished(self, results):        
        self._logger.info("Speedtest finished.")
        self._client.publish(self._mqtt_topic + "/state/running", "0")
        # publish info
        speed_download = results["download"]
        self._client.publish(self._mqtt_topic + "/state/speed_download", speed_download)
        self._client.publish(self._mqtt_topic + "/state/speed_download_formatted", sizeof_fmt(speed_download) + "/s")
        speed_upload = results["upload"]
        self._client.publish(self._mqtt_topic + "/state/speed_upload", speed_upload)
        self._client.publish(self._mqtt_topic + "/state/speed_upload_formatted", sizeof_fmt(speed_upload) + "/s")
        ping = results["ping"]
        self._client.publish(self._mqtt_topic + "/state/ping", ping)
        self._client.publish(self._mqtt_topic + "/state/ping_formatted", "{0} ms".format(ping))
        server_location = results["server"]["name"]
        self._client.publish(self._mqtt_topic + "/state/server_location", server_location)
        server_sponsor = results["server"]["sponsor"]
        self._client.publish(self._mqtt_topic + "/state/server_sponsor", server_sponsor)
        ipaddr = results["client"]["ip"]
        self._client.publish(self._mqtt_topic + "/state/ip", ipaddr)
        isp = results["client"]["isp"]
        self._client.publish(self._mqtt_topic + "/state/isp", isp)
        
    def start(self):
        self._run = True
        # set up MQTT client
        self._client = paho.Client(client_id=self._mqtt_client_id)
        self._client.on_message = self.on_mqtt_recv
        self._client.connect(self._mqtt_broker, 1883)
        self._client.subscribe(self._mqtt_topic + "/command/#")
        self._client.loop_start()
        self._logger.info("MQTT transport configured.")
        self._logger.debug("Broker is '{0}'.".format(self._mqtt_broker))
        self._logger.debug("Client id is '{0}'.".format(self._mqtt_client_id))
        self._logger.debug("Listening for messages with topic '{0}/command'.".format(self._mqtt_topic))
        self._client.publish(self._mqtt_topic + "/state/interval", self._interval)
        # handle incoming RF transmission
        while self._run:
            time.sleep(1)
            if self._speedtest is not None:
                if self._speedtest.finished():
                    results = self._speedtest.get_results()
                    self.on_speedtest_finished(results)
                    self._speedtest = None
            if time.time() - self._last_run >= self._interval:
                self.run_speedtest()

