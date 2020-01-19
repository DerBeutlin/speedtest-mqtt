# -*- coding: utf-8 -*-
from distutils.core import setup


setup(name="speedtestmqtt",
      version="0.0.1",
      description="Speedtest with MQTT interface.",
      author="Sven Festersen",
      author_email="sven@sven-festersen.de",
      packages=["speedtestmqtt"],
      requires=["paho.mqtt", "speedtestcli"],
      scripts=["cli/speedtest-mqtt"]
     )
