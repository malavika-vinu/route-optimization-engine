import streamlit as st
import requests

st.title("Smart Route Optimization Engine")
st.write("Add delivery locations and get the most efficient route.")

if "locations" not in st.session_state:                 #Initialize the session state
    st.session_state["locations"] = []

st.subheader("Add a Location")

col1, col2, col3 = st.columns(3)                        #Created 3 columns each for the location name, x and y coordinates

with col1:
    name = st.text_input("Location Name", placeholder="Name of the Building")
with col2:
    x = st.number_input("X Coordinate", value=0.0)
with col3:
    y = st.number_input("Y Coordinate", value=0.0)

if st.button("Add Location"):
    if name:
        st.session_state["locations"].append({"name": name, "x": x, "y": y})
        st.success(f"{name} added!")
    else:
        st.error("Please enter location name.")


if st.session_state["locations"]:                           #Display if any locations added
    st.subheader("Added Locations")
    for i, loc in enumerate(st.session_state["locations"]):
        st.write(f"{i+1}. {loc["name"]} - ({loc["x"], loc["y"]})")

if st.session_state["locations"]:                           #Clear button to clear the locations added
    if st.button("Clear All"):
        st.session_state["locations"] = []
        st.rerun()

st.divider()

if st.button("Optimize Route"):
    if len(st.session_state["locations"]) < 2:
        st.error("Please add atleast 2 locations.")
    else:
        response = requests.post(
            "http://127.0.0.1:8000/optimize-route", 
            json={"locations": st.session_state["locations"]}
        )
        if response.status_code == 200:
            route = response.json()["route"]
            st.success("Route Optimized!")
            st.subheader("Optimized Route")
            for i, stop in enumerate(route):
                st.write(f"{i+1}. {stop["name"]} - ({stop["x"]}, {stop["y"]})")
        else:
            st.error("Something went wrong. Is the API running?")
