import streamlit as st
import requests
import folium
from streamlit_folium import st_folium

st.title("Smart Route Optimization Engine")
st.write("Add delivery locations and get the most efficient route.")

if "locations" not in st.session_state:                 #Initialize the session state
    st.session_state["locations"] = []
if "result" not in st.session_state:
    st.session_state["result"] = None

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
        st.session_state["result"] = None
        st.rerun()

st.divider()

if st.button("Optimize Route"):
    if len(st.session_state["locations"]) < 2:
        st.error("Please add atleast 2 locations.")
    else:
        with st.spinner("Optimizing route... (OR-Tools searches for up to 5 seconds)"):
            response = requests.post(
                "http://127.0.0.1:8000/optimize-route",
                json={"locations": st.session_state["locations"]}
            )
        if response.status_code == 200:
            st.session_state["result"] = response.json()
        else:
            st.error("Something went wrong. Is the API running?")

if st.session_state["result"]:
    result = st.session_state["result"]
    route = result["nearest_neighbor"]["route"]
    st.success("Route Optimized!")

    nn = result["nearest_neighbor"]
    ort = result["ortools"]

    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("Nearest Neighbor", f"{nn['total_distance']} units")
    with m2:
        st.metric("OR-Tools", f"{ort['total_distance']} units")
    with m3:
        st.metric("Improvement", f"{result['improvement_percent']}%")

    r1, r2 = st.columns(2)
    with r1:
        st.subheader("Nearest Neighbor")
        for i, stop in enumerate(nn["route"]):
            st.write(f"{i+1}. {stop['name']}")
    with r2:
        st.subheader("OR-Tools")
        for i, stop in enumerate(ort["route"]):
            st.write(f"{i+1}. {stop['name']}")

    st.subheader("Route Map")
    st.caption("🔴 Nearest Neighbor (thick)  |  🔵 OR-Tools (thin, on top). Where only one color shows, the routes differ.")
    m = folium.Map(location=[route[0]["lat"], route[0]["lng"]], zoom_start=7)

    for i, stop in enumerate(ort["route"]):
        folium.Marker(
            location=[stop["lat"], stop["lng"]],
            popup=stop["name"],
            tooltip=f"{i+1}. {stop['name']}"
        ).add_to(m)

    nn_points = [[s["lat"], s["lng"]] for s in nn["route"]]
    nn_points.append(nn_points[0])
    folium.PolyLine(nn_points, color="red", weight=6, opacity=0.6, tooltip="Nearest Neighbor").add_to(m)

    or_points = [[s["lat"], s["lng"]] for s in ort["route"]]
    or_points.append(or_points[0])
    folium.PolyLine(or_points, color="blue", weight=2.5, tooltip="OR-Tools").add_to(m)

    st_folium(m, width=700, height=500)