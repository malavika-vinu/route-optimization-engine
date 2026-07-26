import streamlit as st
import requests
import folium
from streamlit_folium import st_folium

st.title("Smart Route Optimization Engine")
st.write("Add delivery locations and get the most efficient route.")

if "locations" not in st.session_state:                 #Initialize the session state
    st.session_state["locations"] = []
if "route" not in st.session_state:
    st.session_state["route"] = None

st.subheader("Add a Location")

col1, col2, col3 = st.columns(3)                        #Created 3 columns each for the location name, x and y coordinates

with col1:
    name = st.text_input("Location Name", placeholder="Name of the Building")
with col2:
    lat = st.number_input("Latitude", value=0.0, format="%.4f")
with col3:
    lng = st.number_input("Longitude", value=0.0, format="%.4f")

if st.button("Add Location"):
    if name:
        st.session_state["locations"].append({"name": name, "lat": lat, "lng": lng})
        st.success(f"{name} added!")
    else:
        st.error("Please enter location name.")

if st.session_state["locations"]:                           #Display if any locations added
    st.subheader("Added Locations")
    for i, loc in enumerate(st.session_state["locations"]):
        st.write(f"{i+1}. {loc['name']} - ({loc['lat']}, {loc['lng']})")

if st.session_state["locations"]:                           #Clear button to clear the locations added
    if st.button("Clear All"):
        st.session_state["locations"] = []
        st.session_state["route"] = None
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
            st.session_state["route"] = response.json()["route"]
        else:
            st.error("Something went wrong. Is the API running?")

if st.session_state["route"]:
    route = st.session_state["route"]
    st.success("Route Optimized!")
    st.subheader("Optimized Route")
    for i, stop in enumerate(route):
        st.write(f"{i+1}. {stop['name']} - ({stop['lat']}, {stop['lng']})")

    st.subheader("Route Map")
    m = folium.Map(location=[route[0]["lat"], route[0]["lng"]], zoom_start=7)

    for i, stop in enumerate(route):
        folium.Marker(
            location=[stop["lat"], stop["lng"]],
            popup=stop["name"],
            tooltip=f"{i+1}. {stop['name']}"
        ).add_to(m)

    points = [[stop["lat"], stop["lng"]] for stop in route]
    points.append(points[0])
    folium.PolyLine(points, color="red", weight=2.5).add_to(m)

    st_folium(m, width=700, height=500)