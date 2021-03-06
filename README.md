# MQTT Dropbox
Takes MQTT messages with image path and uploads them to Dropbox before sending acknowledgement MQTT message with
URL to upload

### Environment variables
Pass the following environment vairables to execution environment
| Settings | Description | Inputs |
| :----: | --- | --- |
| `MQTT_BROKER` | MQTT Broker address | `mqtt.test.local` |
| `MQTT_PORT` | MQTT Broker port | `1883` |
| `MQTT_SUB_TOPIC` | MQTT Topic to subscribe to | `test/messages` |
| `INPUT_PATH` | Sub directory with input files | `input` |
| `DROPBOX_TOKEN` | Dropbox API Token | `SoMeSeCrEt988766553` |
| `DROPBOX_PATH` | Future use | `/some/path` |

### Requirements
```sh
pip install -p requirements.txt
```

### Execution 
```sh
python3 .\main.py
```

### Docker Compose
```sh 
mqttdropboxbot:
    image: stuartgraham/mqttdropboxbot
    container_name: mqttdropboxbot
    environment:
        - INPUT_PATH=input
        - MQTT_BROKER=mqtt.test.local
        - MQTT_PORT=1883
        - MQTT_PUB_TOPIC=test/moremessages
        - MQTT_SUB_TOPIC=test/evenmoremessages
        - DROPBOX_TOKEN=SoMeSeCrEt988766553
    volumes:
        - input-storage:/app/input:ro
    restart: always
```