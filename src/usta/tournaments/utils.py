import logging
import os

from geocodio import GeocodioClient
from geopy.distance import geodesic

logging.basicConfig(
    level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s"
)


def calculate_distance(location1: str, location2: str) -> int:
    api_key = os.getenv("GEOCODIO_API_KEY")
    client = GeocodioClient(api_key)

    try:
        # Geocode the first location
        loc1 = client.geocode(location1)
        if not loc1:
            logging.error(f"Could not geocode location: {location1}")
            return None

        # Geocode the second location
        loc2 = client.geocode(location2)
        if not loc2:
            logging.error(f"Could not geocode location: {location2}")
            return None

        # Extract latitude and longitude
        coords1 = (loc1.coords[0], loc1.coords[1])
        coords2 = (loc2.coords[0], loc2.coords[1])

        # Calculate the geodesic distance in miles
        distance_miles = geodesic(coords1, coords2).miles
        return round(distance_miles)

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return None
