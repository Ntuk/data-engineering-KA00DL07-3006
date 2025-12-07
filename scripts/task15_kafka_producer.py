import requests
import json
import time
from kafka import KafkaProducer

URL = "https://api.porssisahko.net/v2/latest-prices.json"
TOPIC = "electricity_prices"

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

last_price = None

print("Starting electricity price producer...")

while True:
    try:
        data = requests.get(URL).json()
        latest = data["prices"][0]
        price = latest["price"]

        if price != last_price:
            for entry in data["prices"]:
                producer.send(TOPIC, entry)
                producer.flush()
                print("Sent:", entry)
            last_price = price
        else:
            print("No price change")

    except Exception as e:
        print("Error:", e)

    time.sleep(30)
