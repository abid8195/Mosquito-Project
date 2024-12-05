import ssl
import random
from paho.mqtt import client as mqtt_client


broker = '136.186.230.70'
port = 8883


subscribe_topic_private = "abid/#"
subscribe_topic_public = "public/#"


client_id = f'subscribe-{random.uniform(0, 1000)}'


username = 'abid'
password = 'password'


ca_cert_path = 'root.crt'
client_cert = 'IntCert.crt'
client_key = 'intcert.key'


def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")

            client.subscribe(subscribe_topic_private)
            client.subscribe(subscribe_topic_public)
            print(f"Subscribed to topics: '{subscribe_topic_private}' and '{subscribe_topic_public}'")
        else:
            print(f"Failed to connect, return code {rc}")

    def on_message(client, userdata, msg):

        print(f"Received message from topic: {msg.topic}")
        print(f"Message: {msg.payload.decode('utf-8')}")


    client = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION1, client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.on_message = on_message


    client.tls_set(certfile=client_cert, keyfile=client_key, ca_certs=ca_cert_path, tls_version=ssl.PROTOCOL_TLSv1_2)
    client.tls_insecure_set(False)


    client.connect(broker, port)
    return client



def run():
    client = connect_mqtt()
    client.loop_forever()

if __name__ == '__main__':
    run()
