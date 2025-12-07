# Task 15 – Kafka Streaming Pipeline (Electricity Prices)

**Objective:**  
Create a small streaming pipeline using Kafka:  
- A producer that sends updated electricity price data  
- A consumer that writes incoming messages to a file  
- A Streamlit app that visualizes the results

## Steps

### 1. Producer  
Fetches data from:  
`https://api.porssisahko.net/v2/latest-prices.json`  

Sends all entries to the Kafka topic **`electricity_prices`** whenever a new price appears.

Script:  
`scripts/task15_kafka_producer.py`

---

### 2. Consumer  
Listens to the Kafka topic and appends each received message to:
reports/task15_kafka/prices_output.txt


Script:  
`scripts/task15_kafka_consumer.py`

---

### 3. Visualization  
Reads the saved file and displays:

- A line chart of electricity prices  
- A table of all received rows  

Script:  
`scripts/task15_streamlit.py`

## Instructions to run

Run the components **in this order**:

### 1. Start Kafka
In the `kafka/` folder:
```sh
docker compose up -d
``` 

### 2. Start the Consumer
In the root folder:
```
python scripts/task15_kafka_consumer.py
```

### 3. Start the Producer
In the root folder:
```
python scripts/task15_kafka_producer.py
```

### 4. Start Streamlit Dashboard
In the root folder:
```
streamlit run scripts/task15_streamlit.py
```
Dashboard URL:
http://localhost:8501