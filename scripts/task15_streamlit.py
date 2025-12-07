import streamlit as st
import pandas as pd
import json

st.title("Electricity Price Stream")

with open("reports/task15_kafka/prices_output.txt") as f:
    rows = [json.loads(line) for line in f]

df = pd.DataFrame(rows)

st.line_chart(df["price"])
st.dataframe(df)
