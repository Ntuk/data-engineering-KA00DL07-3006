from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    "electricity_prices",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="latest",
    value_deserializer=lambda v: json.loads(v.decode("utf-8"))
)

print("Listening for messages...")

for msg in consumer:
    data = msg.value
    with open("reports/task15_kafka/prices_output.txt", "a") as f:
        f.write(json.dumps(data) + "\n")
    print("Saved:", data)
