# Smart Route Optimization Engine

A web app that takes a list of delivery locations and works out a short route that visits all of them and returns to the start. It runs two methods on the same locations so you can compare them.

**Live demo:** https://route-optimization-engine.streamlit.app
**Backend API:** https://route-optimization-engine-ipgb.onrender.com

> The backend runs on a free Render plan, which goes to sleep after about 15 minutes without use. The first click after a long break can take up to a minute while it wakes up.

## Screenshots

**Comparison of both methods**
![Comparison results](screenshots/comparison-results.png)

**Route on the map**
![Route map](screenshots/route-map.png)

## What it does

- You type in location names with latitude and longitude.
- You click **Optimize Route**. The app runs **both** methods on the same locations.
- It shows the total loop distance for each method, the percentage improvement, the visiting order of each, and a map with the route drawn on it.

## The two methods

- **Nearest Neighbor:** from where you are, always go to the closest stop not yet visited. It is very fast but can make poor choices.
- **OR-Tools:** Google's routing library. It starts with a route and keeps improving it for a few seconds (Guided Local Search). It is slower but can find shorter routes.

## Benchmark result

Tested on 8 cities along the Kerala coast: Thiruvananthapuram, Kollam, Alappuzha, Kochi, Thrissur, Palakkad, Kozhikode and Kannur.

| Method | Total distance |
|---|---|
| Nearest Neighbor | 8.1352 |
| OR-Tools | 7.7457 |

OR-Tools gave a route **4.79% shorter**.

These cities lie almost in a straight line, so Nearest Neighbor already does well and there is little left to improve. With cities spread out in several separate clusters, the gap is usually larger.

Distances are straight-line distances measured in latitude/longitude degrees, not kilometres. That is fine for comparing methods, but it is not road distance.

## How it is built

- `src/algorithm.py`: distance calculation, Nearest Neighbor, OR-Tools solver, total distance
- `main.py`: FastAPI backend with the `/optimize-route` endpoint (hosted on Render)
- `app.py`: Streamlit frontend with a Folium map (hosted on Streamlit Community Cloud)

## Run it on your own computer

1. Download the project and open a terminal in its folder.
2. Create and activate a virtual environment (a private space for this project's tools):
   ```
   python -m venv venv
   venv\Scripts\activate
   ```
3. Install the requirements:
   ```
   pip install -r requirements.txt
   ```
4. Start the backend in one terminal:
   ```
   uvicorn main:app --reload
   ```
5. Start the app in a second terminal:
   ```
   streamlit run app.py
   ```

## Ideas for later

- Use haversine distance to get real kilometres
- Paste or upload many locations at once (CSV)