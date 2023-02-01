#this code is just me testing if this could work with the regular paho, turns out fuck no it cant, so the async wrapper needs to be applied to this soontm

import time, nuggbot
import paho.mqtt.client as paho
from paho import mqtt

def on_connect(client, userdata, flags, rc, properties=None):
    return(True)

def on_message(client, userdata, msg):
    nuggbot.publish_chan(str(msg.payload))

if __name__ == "__main__":

    client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
    client.on_connect = on_connect

    client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
    client.username_pw_set("2", "3")
    client.connect("4", 8883)

    client.on_message = on_message
    client.subscribe("constellation/1", qos=0)
    client.loop_forever()

async def publish_mqtt(msg: str):
    client.publish("nuggtech/1", payload=msg, qos=0)