import requests
import pandas as pd
import os
import time

# Read API token from environment
MAPBOX_TOKEN = os.getenv("MAPBOX_TOKEN")
if MAPBOX_TOKEN is None:
    raise ValueError("MAPBOX_TOKEN not found. Please set it as an environment variable.")

def fetch_satellite_image(lat, lon, save_path, zoom=18, size="256x256"):
    
    if os.path.exists(save_path):
        return  # Skip if already downloaded

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


def fetch_images_for_dataframe(df, output_dir, sleep_time=0.2, max_images=None):

    os.makedirs(output_dir, exist_ok=True)

    for i, (_, row) in enumerate(df.iterrows()):
        if max_images is not None and i >= max_images:
            break

        img_id = row["id"]
        save_path = os.path.join(output_dir, f"{img_id}.png")

        fetch_satellite_image(
            lat=row["lat"],
            lon=row["long"],
            save_path=save_path
        )

        time.sleep(sleep_time)

    print(f"download done at {output_dir}")



