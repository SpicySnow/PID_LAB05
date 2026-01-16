from time import sleep
from json import dumps
from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable
from kafka.errors import KafkaTimeoutError
import os
import random
import time

while True:
    try:
        producer = KafkaProducer(
            bootstrap_servers=[os.environ.get("BROKER_BOOTSTRAP","127.0.0.1")],
            value_serializer=lambda x:
               dumps(x).encode('utf-8'))

        BASE_VOLTAGE = 230.0
        BASE_FREQ = 50.0
        NOISE_STD = 0.1

        v_true = BASE_VOLTAGE

        while True:
            moment = int(time.time() * 1000)

            v_true += random.gauss(0, 0.03)
            # pull toward base
            v_true += 0.02 * (BASE_VOLTAGE - v_true)

            # measurement noise
            voltage = v_true + random.gauss(0, 0.10)

            frequency = BASE_FREQ - 0.02 * (v_true - BASE_VOLTAGE) + random.gauss(0, 0.005)

            # rare sensor glitch
            if random.random() < 0.002:
                voltage += random.uniform(-10, 10)

            frequency = 50.0 - 0.02 * (voltage - 230) + random.gauss(0, 0.005)

            data = {'time': moment, 'V1': voltage, 'F': frequency}
            producer.send(os.environ.get("BROKER_TOPIC", "data"), value=data)

            sleep(int(os.environ.get("SLEEP_MS",1000))/1000)

    except NoBrokersAvailable:
        sleep(5)

    except KafkaTimeoutError:
        sleep(5)
