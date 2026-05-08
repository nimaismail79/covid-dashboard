import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import json

st.title("COVID-19 Dashboard")

st.header("Hospital Admissions & Deaths (Rolling Mean)")

# Load JSON files
with open("admissions.json") as f:
    admissions_data = json.load(f)

with open("deaths.json") as f:
    deaths_data = json.load(f)

# Convert to DataFrames
admissions_df = pd.DataFrame(admissions_data)
deaths_df = pd.DataFrame(deaths_data)

# Select important columns
admissions_df = admissions_df[["date", "metric_value"]]
deaths_df = deaths_df[["date", "metric_value"]]

# Rename columns
admissions_df.columns = ["date", "admissions"]
deaths_df.columns = ["date", "deaths"]

# Merge datasets
timeseriesdf = pd.merge(
    admissions_df,
    deaths_df,
    on="date"
)

# Convert dates
timeseriesdf["date"] = pd.to_datetime(timeseriesdf["date"])

# Sidebar filter
choice = st.selectbox(
    "Select graph view",
    ["Both", "Admissions only", "Deaths only"]
)

# Plot graph
fig, ax = plt.subplots(figsize=(10,5))

if choice == "Admissions only":
    ax.plot(
        timeseriesdf["date"],
        timeseriesdf["admissions"],
        label="Admissions"
    )

elif choice == "Deaths only":
    ax.plot(
        timeseriesdf["date"],
        timeseriesdf["deaths"],
        label="Deaths",
        color="red"
    )

else:
    ax.plot(
        timeseriesdf["date"],
        timeseriesdf["admissions"],
        label="Admissions"
    )

    ax.plot(
        timeseriesdf["date"],
        timeseriesdf["deaths"],
        label="Deaths",
        color="red"
    )

ax.set_title("Daily COVID-19 Hospital Admissions and Deaths")
ax.set_xlabel("Date")
ax.set_ylabel("Rolling Mean")
ax.legend()

st.pyplot(fig)

# Boxplot section
st.subheader("Distribution Comparison")

metric_choice = st.radio(
    "Choose metric",
    ["Both", "Admissions only", "Deaths only"]
)

fig2, ax2 = plt.subplots(figsize=(8,5))

if metric_choice == "Both":
    timeseriesdf[["admissions", "deaths"]].boxplot(ax=ax2)

elif metric_choice == "Admissions only":
    timeseriesdf[["admissions"]].boxplot(ax=ax2)

else:
    timeseriesdf[["deaths"]].boxplot(ax=ax2)

ax2.set_title("Distribution Comparison")
ax2.set_ylabel("Rolling Mean")

st.pyplot(fig2)

# Show raw data
with st.expander("View raw data"):
    st.dataframe(timeseriesdf)
