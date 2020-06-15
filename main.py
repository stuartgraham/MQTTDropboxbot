import paho.mqtt.client as paho
import paho.mqtt.publish as publish
import time
import os
import json
import datetime
import logging
import dropbox
import threading

# .ENV FILE FOR TESTING
#if os.path.exists('.env'):
#    from dotenv import load_dotenv
#    load_dotenv()

# GLOBALS
MQTT_BROKER = os.environ.get('MQTT_BROKER','')
MQTT_PORT = int(os.environ.get('MQTT_PATH', 1883))
MQTT_SUB_TOPIC = os.environ.get('MQTT_SUB_TOPIC','')
MQTT_PUB_TOPIC = os.environ.get('MQTT_PUB_TOPIC','')
DROPBOX_TOKEN = os.environ.get('DROPBOX_TOKEN','')
INPUT_PATH = os.environ.get('INPUT_PATH','input')
DROPBOX_PATH = os.environ.get('DROPBOX_PATH','input')

BASE_DIR = os.getcwd()
INPUT_PATH = os.path.join(BASE_DIR, INPUT_PATH)


def post_to_dropbox(image, confidence, category):
    dbx = dropbox.Dropbox(DROPBOX_TOKEN)
    logging.debug("Uploading file {}".format(str(image)))
    try:
        os.chdir(INPUT_PATH)
        with open(image, 'rb') as f:
            response = dbx.files_upload(f.read(), "/" + image, mute=True)
            logging.debug("Response : {}".format(str(response)))
            metadata = dbx.sharing_create_shared_link("/" + image)
            print(metadata)
            push_mqtt_message({'url': metadata.url, 'category': category, 'confidence': float(confidence)})

    except Exception as err:
        print("Failed to upload {}, error : {}".format(image, err))

    os.chdir(BASE_DIR)
 

# PUB MQTT
def push_mqtt_message(message):
    publish.single(MQTT_PUB_TOPIC,
        payload=json.dumps(message),
        hostname=MQTT_BROKER,
        client_id="mqtt-dropbox-bot",
        port=MQTT_PORT)


# SUB MQTT
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(MQTT_SUB_TOPIC)

def on_message(client, userdata, msg):
    logging.info("Received : {} convert to json".format(str(msg.payload))) 
    message = msg.payload.decode('utf-8')
    logging.debug("message : {}".format(str(message))) 
    message = json.loads(message)
    category = message['category']
    logging.debug("json_category : {}".format(str(category))) 
    confidence = message['confidence']
    logging.debug("json_confidence : {}".format(str(confidence)))
    image = message['image']
    logging.debug("json_image : {}".format(str(image)))
    post_to_dropbox(image, confidence, category)
    uploader = threading.Thread(target=post_to_dropbox(image, confidence, category))
    uploader.start()


def main():
    logging.basicConfig(filename='app.log', level=logging.DEBUG, format='%(asctime)s %(message)s')
    logging.info("STARTING MQTT Dropbox bot")
    client = paho.Client("mqtt-dropbox-bot")
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_forever()

# Main Exectution
main()