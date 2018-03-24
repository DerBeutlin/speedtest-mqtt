# speedtest-mqtt
Internet connection speedtest based on the speedtest-cli library
(https://pypi.python.org/pypi/speedtest-cli/). Requires Python 3,
speedtest-cli and paho-mqtt.

## Installation
Use the setup script to install:

    python setup.py install
    
## Usage
The setup script installs the `speedtest-mqtt` command line program. Usage:

    speedtest-mqtt --broker <mqtt_broker> --clientid <mqtt_client_id> --topic <mqtt_topic>
    
All paramters are optional.
Example:

    cul-mqtt --broker localhost
    
The default client id ist "speedtest", the default topic "sppedtest".

By default, speedtests are run every hour. To run a speedtest manually,
publish the message "run" to "<mqtt_topic>/command/run". To change the
automatic speedtest interval, publish the value in seconds to
"<mqtt_topic>/command/interval".

## TODO
 * implement authentication
 * implement TLS
