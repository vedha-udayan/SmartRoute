
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# SMARTROUTE - TRAFFIC OPTIMIZATION

st.set_page_config(page_title="SmartRoute", page_icon="🚦")

st.title("🚦 SmartRoute")
st.subheader("Traffic and Metro Express Optimization")

st.write("Reducing traffic congestion in Mauritius.")

st.info("This project uses simulated traffic data.")

# STEP 1: Traffic data

data = {
    "Route": ["Port Louis - Rose Hill",
              "Rose Hill - Quatre Bornes",
              "Quatre Bornes - Curepipe"],

    "Vehicles": [3600, 3300, 3500],

    "Capacity": [3000, 2800, 2900],

    "Travel_Time": [9, 8, 11]
}

df = pd.DataFrame(data)

# STEP 2: User settings

st.sidebar.header("Settings")

traffic = st.sidebar.selectbox(
    "Traffic Period",
    ["Morning Peak", "Afternoon", "Evening Peak"]
)

if traffic == "Morning Peak":
    multiplier = 1.2
elif traffic == "Afternoon":
    multiplier = 0.8
else:
    multiplier = 1.3

shift = st.sidebar.slider(
    "People shifting to Metro (%)", 0, 30, 10
)

signal = st.sidebar.slider(
    "Signal improvement (%)", 0, 20, 10
)

bus_frequency = st.sidebar.slider(
    "Bus frequency (minutes)", 3, 20, 8
)

# STEP 3: Calculate traffic

df["Traffic_Before"] = df["Vehicles"] * multiplier

df["Traffic_After"] = (
    df["Traffic_Before"] * (1 - shift / 100)
)

# STEP 4: Calculate travel time

df["Time_Before"] = (
    df["Travel_Time"] *
    (1 + 0.5 * (df["Traffic_Before"] / df["Capacity"] - 1).clip(lower=0))
)

df["Time_After"] = (
    df["Travel_Time"] *
    (1 + 0.5 * (
        df["Traffic_After"] /
        (df["Capacity"] * (1 + signal / 100)) - 1
    ).clip(lower=0))
)

df["Time_Saved"] = df["Time_Before"] - df["Time_After"]

# STEP 5: Display results

st.header("📊 Traffic Results")

total_before = df["Time_Before"].sum()
total_after = df["Time_After"].sum()

col1, col2, col3 = st.columns(3)

col1.metric("Before", f"{total_before:.1f} min")
col2.metric("After", f"{total_after:.1f} min")
col3.metric("Time Saved", f"{total_before-total_after:.1f} min")

st.subheader("Route Analysis")

st.subheader("Route Analysis")

for index, row in df.iterrows():

    st.write("Route:", row["Route"])

    st.write("Traffic Before:", round(row["Traffic_Before"], 2))

    st.write("Traffic After:", round(row["Traffic_After"], 2))

    st.write("Travel Time Before:", round(row["Time_Before"], 2), "minutes")

    st.write("Travel Time After:", round(row["Time_After"], 2), "minutes")

    st.write("Time Saved:", round(row["Time_Saved"], 2), "minutes")

    st.write("-----------------------------")

# STEP 6: Congestion detection

st.header("🚗 Congestion Detection")

for i, row in df.iterrows():

    if row["Traffic_Before"] > row["Capacity"]:
        st.error(row["Route"] + " - High Congestion")
    else:
        st.success(row["Route"] + " - Normal Traffic")

# STEP 7: Feeder bus recommendations

st.header("🚌 Feeder Bus Planning")

commuters = df["Traffic_Before"].iloc[0] * shift / 100 * 1.2

buses_needed = round(commuters / 50)

buses_available = 60 / bus_frequency

st.write("Estimated commuters shifting:", round(commuters))
st.write("Estimated buses needed per hour:", buses_needed)
st.write("Buses scheduled per hour:", round(buses_available, 1))

if buses_available >= buses_needed:
    st.success("Bus capacity is sufficient.")
else:
    st.warning("Increase feeder bus frequency.")

# STEP 8: Metro Express comparison

st.header("🚆 Metro Express")

metro_time = 28
feeder_time = 7
waiting_time = bus_frequency / 2
walking_time = 5

total_metro_time = (
    metro_time + feeder_time +
    waiting_time + walking_time
)

st.write("Estimated Metro Express journey:", total_metro_time, "minutes")

if total_metro_time < total_after:
    st.success("Metro Express is faster in this simulation.")
else:
    st.info("Car travel is faster in this simulation.")

# STEP 9: Graph

st.header("📈 Travel Time Comparison")

fig, ax = plt.subplots()

ax.bar(df["Route"], df["Time_Before"], label="Before")
ax.bar(df["Route"], df["Time_After"], label="After")

ax.set_ylabel("Travel Time (Minutes)")
ax.set_xlabel("Routes")
ax.set_title("Before vs After Optimization")

ax.legend()
plt.xticks(rotation=15)
plt.tight_layout()

st.pyplot(fig)

# STEP 10: Final recommendation

st.header("💡 Recommendations")

st.write("1. Improve traffic signal timings.")
st.write("2. Increase feeder bus frequency during peak hours.")
st.write("3. Encourage people to use Metro Express.")
st.write("4. Monitor traffic congestion regularly.")

st.success("Thank you for using SmartRoute!")
