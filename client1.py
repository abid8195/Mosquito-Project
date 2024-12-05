import random
import time
import ssl
from paho.mqtt import client as mqtt_client


broker = '136.186.230.70'
port = 8883

publish_topic1 = "abid/device1"
publish_topic2 = "abid/device2"

subscribe_topic = "public/#"



client_id = f'publish-{random.uniform(0, 1000)}'


username = 'abid'
password = 'password'


ca_cert_path = 'root.crt'
client_cert = 'IntCert.crt'
client_key = 'intcert.key'


def connect_mqtt():
    def on_connect(client, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
            client.subscribe(subscribe_topic)   # Subscribe to the first publish topic
        else:
            print(f"Failed to connect, return code {rc}")

    def on_message(msg):
        print(f"Received message on topic: {msg.topic}")
        print(f"Message: {msg.payload.decode('utf-8')}")


    client = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION2, client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.on_message = on_message


    client.tls_set(certfile=client_cert, keyfile=client_key, ca_certs=ca_cert_path, tls_version=ssl.PROTOCOL_TLSv1_2)  # Use appropriate TLS version
    client.tls_insecure_set(False)


    client.connect(broker, port)
    return client


def publish(client):
    msg_count = 1
    while True:
        time.sleep(1)
        temperature = random.randint(0, 200)
        msg = f"Temperature: {temperature}" + chr(176) + "C"


        if temperature > 80:
            warning_msg = "Warning: High Temperatures"
            result_warning = client.publish(publish_topic1, warning_msg, 0, True)
            status_warning = result_warning.rc
            if status_warning == mqtt_client.MQTT_ERR_SUCCESS:
                print(f"Send warning: '{warning_msg}' to topic '{publish_topic1}'")


        result1 = client.publish(publish_topic1, msg, 0, True)
        status1 = result1.rc
        if status1 == mqtt_client.MQTT_ERR_SUCCESS:
            print(f"Send '{msg}' to topic '{publish_topic1}'")
        else:
            print(f"Failed to send message to topic {publish_topic1}")


        result2 = client.publish(publish_topic2, msg, 0, True)
        status2 = result2.rc
        if status2 == mqtt_client.MQTT_ERR_SUCCESS:
            print(f"Send '{msg}' to topic '{publish_topic2}'")
        else:
            print(f"Failed to send message to topic {publish_topic2}")

        msg_count += 1



def run():
    random.seed(10)
    client = connect_mqtt()
    client.loop_start()
    publish(client)
    client.loop_forever()

if __name__ == '__main__':
    run()
