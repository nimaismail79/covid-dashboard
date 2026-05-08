import streamlit as st
import pandas as pd
import plotly.express as px
import json

st.title("COVID-19 Dashboard")

st.header("Hospital Admissions & Deaths")

with open("admissions.json") as f:
    admissions_data = json.load(f)

with open("deaths.json") as f:
    deaths_data = json.load(f)

admissions_df = pd.DataFrame(admissions_data)
deaths_df = pd.DataFrame(deaths_data)

st.subheader("Admissions Data")
st.dataframe(admissions_df.head())

st.subheader("Deaths Data")
st.dataframe(deaths_df.head())

fig = px.line(
    admissions_df,
    x=admissions_df.columns[0],
    y=admissions_df.columns[1],
    title="Admissions Trend"
)

st.plotly_chart(fig)
