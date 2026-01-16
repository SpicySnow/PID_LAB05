import os
import json
import time
from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable


# TODO: podmienić na prawdziwe funkcje
try:
    from db_mocks import save_raw, update_latest, increment_count
except ImportError:
    print("Brak modułów")
    exit(1)

# ENV conf (upewnić się czy jest tak jak w docker-compose później(
KAFKA_BROKER = os.environ.get("KAFKA_BROKER", "localhost:9092")
KAFKA_TOPIC = os.environ.get("KAFKA_TOPIC", "measurements")
KAFKA_GROUP = os.environ.get("KAFKA_GROUP", "measurement_group")

def create_consumer():
    """funkcja próbująca połączyć się z Kafką z mechanizmem retry"""
    consumer = None
    while not consumer:
        try:
            print(f"Próba połączenia z Kafka ({KAFKA_BROKER})...")
            consumer = KafkaConsumer(
                KAFKA_TOPIC,
                bootstrap_servers=KAFKA_BROKER,
                group_id=KAFKA_GROUP,
                auto_offset_reset='latest',
                value_deserializer=lambda m: json.loads(m.decode('utf-8'))
            )
            print("Połączono z Kafką")
        except NoBrokersAvailable:
            print("Kafka niedostępna. Ponowna próba za 5s...")
            time.sleep(5)
    return consumer

def main():
    consumer = create_consumer()

    print(f"Rozpoczynam nasłuchiwanie na kanale: {KAFKA_TOPIC}")
    
    for message in consumer:
        try:
            data = message.value
            
            # walidacja czy mamy wszystkie pola
            if not all(k in data for k in ("generator", "ts", "V1", "F")):
                print(f"Błędny format wiadomości: {data}")
                continue

            generator = data["generator"]
            ts = data["ts"]
            v1 = data["V1"]
            f = data["F"]

            # Wywołanie funkcji (na razie mockowe)
            # 1. zapis surowych danych (Osoba 4)
            save_raw(generator, ts, v1, f)

            # 2. aktualizacja 'ostatnich' wartości (Osoba 5)
            update_latest(generator, ts, v1, f)

            # 3. zliczanie próbek (Osoba 6)
            increment_count(generator, ts)

        except Exception as e:
            print(f"Błąd przetwarzania wiadomości: {e}")

if __name__ == "__main__":
    main()