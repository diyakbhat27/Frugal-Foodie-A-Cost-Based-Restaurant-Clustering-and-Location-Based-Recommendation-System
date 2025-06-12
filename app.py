from flask import Flask, request, jsonify, render_template
import requests
import pandas as pd
from sklearn.cluster import KMeans

app = Flask(__name__)

# Google API key
PLACES_API_KEY = "YOUR_GOOGLE_API_KEY_HERE"  # Replace with your actual Google API key

# ✅ Load and preprocess the dataset
df = pd.read_csv(r"path/to/your/zomato.csv")  # Update with the correct path to your dataset
df.columns = df.columns.str.strip().str.lower()
df.rename(columns={'approx_cost(for two people)': 'price'}, inplace=True)

# Clean price column
df['price'] = df['price'].astype(str).str.replace(r'[₹,]', '', regex=True)
df['price'] = pd.to_numeric(df['price'], errors='coerce') / 2  # for per person cost
df.dropna(subset=['price'], inplace=True)

# KMeans clustering for budget segmentation
X = df[['price']]
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
df['cluster'] = kmeans.fit_predict(X)

# Convert area name to coordinates
def get_lat_lon_from_area(area_name):
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {"address": area_name, "key": PLACES_API_KEY}
    response = requests.get(url, params=params).json()
    if response["status"] == "OK":
        location = response["results"][0]["geometry"]["location"]
        return location["lat"], location["lng"]
    return None, None

# Get nearby restaurants from Google Places
def get_nearby_restaurants(lat, lon, radius=3000):
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        "location": f"{lat},{lon}",
        "radius": radius,
        "type": "restaurant",
        "key": PLACES_API_KEY
    }
    response = requests.get(url, params=params)
    return response.json().get("results", [])

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/recommend", methods=["POST"])
def recommend():
    data = request.get_json()

    # Input checks
    try:
        budget = float(data["budget"])
        radius_km = float(data["radius"])
    except (ValueError, KeyError):
        return jsonify({"error": "Invalid input format for budget or radius."})

    # Reject budget less than 50
    if budget < 50:
        return jsonify({"error": "Budget too Low"})

    location_mode = data.get("locationMode", "")
    lat, lon = None, None

    # Manual vs Automatic location input
    if location_mode == "manual":
        area = data.get("area", "")
        lat, lon = get_lat_lon_from_area(area)
        if lat is None or lon is None:
            return jsonify({"error": "Could not find the location. Please try another area."})
    else:
        lat = data.get("latitude")
        lon = data.get("longitude")
        if lat is None or lon is None:
            return jsonify({"error": "Geolocation not provided."})

    radius_m = int(radius_km * 1000)

    # heck if budget is above all cluster centers
    cluster_centers = kmeans.cluster_centers_.flatten()
    if budget > cluster_centers.max():
        top_df = df.sort_values(by='price', ascending=False).head(20)
        nearby_places = get_nearby_restaurants(lat, lon, radius=radius_m)

        matched_results = []
        seen = set()

        for place in nearby_places:
            name = place.get("name", "").strip()
            address = place.get("vicinity", "").strip()
            unique_key = (name.lower(), address.lower())
            if unique_key in seen:
                continue
            seen.add(unique_key)

            # Even if not in dataset, include it
            matched_results.append({
                "name": name,
                "address": address,
                "rating": place.get("rating", "N/A"),
                "map_link": f"https://www.google.com/maps/search/?q={name.replace(' ', '+')}+{address.replace(' ', '+')}"
            })

            if len(matched_results) == 5:
                break

        return jsonify({"results": matched_results})

    # Predict cluster and filter dataset
    cluster = kmeans.predict([[budget]])[0]
    price_min = budget * 0.8
    price_max = budget * 1.2
    clustered_df = df[(df['cluster'] == cluster) & (df['price'] >= price_min) & (df['price'] <= price_max)].copy()

    nearby_places = get_nearby_restaurants(lat, lon, radius=radius_m)

    matched_results = []
    seen = set()

    for place in nearby_places:
        name = place.get("name", "").strip()
        address = place.get("vicinity", "").strip()
        unique_key = (name.lower(), address.lower())
        if unique_key in seen:
            continue
        seen.add(unique_key)

        matched_results.append({
            "name": name,
            "address": address,
            "rating": place.get("rating", "N/A"),
            "map_link": f"https://www.google.com/maps/search/?q={name.replace(' ', '+')}+{address.replace(' ', '+')}"
        })

    if not matched_results:
        return jsonify({"error": "No Restaurants Found"})

    return jsonify({"results": matched_results})

if __name__ == "__main__":
    app.run(debug=True)