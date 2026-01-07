import requests
import pandas as pd
import os
import time

MAPBOX_TOKEN = os.getenv("MAPBOX_TOKEN")
if MAPBOX_TOKEN is None:
    raise ValueError("MAPBOX_TOKEN not found. Please set it as an environment variable.")

def fetch_satellite_image(lat, lon, save_path):
    zoom = 18
    size = "256x256"

    if os.path.exists(save_path):
        return

    url = (
        f"https://api.mapbox.com/styles/v1/mapbox/satellite-v9/static/"
        f"{lon},{lat},{zoom}/{size}"
        f"?access_token={MAPBOX_TOKEN}"
    )

    response = requests.get(url)

    if response.status_code == 200:
        with open(save_path, "wb") as f:
            f.write(response.content)
    else:
        print(f"Failed ({response.status_code}) for lat={lat}, lon={lon}")

df = pd.read_excel("train(1).xlsx")

os.makedirs("satellite_images", exist_ok=True)

for idx, row in df.head(300).iterrows():  
    img_id = row['id']
    save_path = f"satellite_images/{img_id}.png"

    fetch_satellite_image(
        lat=row["lat"],
        lon=row["long"],
        save_path=save_path
    )

    time.sleep(0.2)

print("download done")
