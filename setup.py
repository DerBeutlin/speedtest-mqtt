# -*- coding: utf-8 -*-
from distutils.core import setup
from culmqtt import __version__ as ver


setup(name="speedtestmqtt",
      version=ver,
      description="Speedtest with MQTT interface.",
      author="Sven Festersen",
      author_email="sven@sven-festersen.de",
      packages=["speedtestmqtt"],
      requires=["paho.mqtt", "speedtestcli"],
      scripts=["cli/speedtest-mqtt"]
     )
