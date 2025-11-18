import streamlit as st
import pandas as pd

df = pd.read_csv("data/polar_summary.csv")

st.title("Polar Training Summary Dashboard")

st.metric("Total Exercises", len(df))
st.metric("Total Distance (km)", round(df["distance_exercise"].sum() / 1000, 2))
st.metric("Total Calories", int(df["calories"].sum()))

st.subheader("Average HR Over Time")
st.line_chart(df[["avg_hr_total"]])

st.subheader("Calories per Exercise")
st.bar_chart(df[["calories"]])

st.subheader("Distance per Exercise (km)")
st.bar_chart(df["distance_exercise"] / 1000)
