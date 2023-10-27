import phonenumbers
from phonenumbers import geocoder, carrier
import folium
from opencage.geocoder import OpenCageGeocode

def get_location_and_service_provider(phone_number):
    try:
        parsed_number = phonenumbers.parse(phone_number)
        location = geocoder.description_for_number(parsed_number, "en")
        service_provider = carrier.name_for_number(parsed_number, "en")
        return location, service_provider
    except:
        return None, None

def get_lat_lng(location, api_key):
    geocoder_api = OpenCageGeocode(api_key)
    results = geocoder_api.geocode(location)
    if results:
        return results[0]['geometry']['lat'], results[0]['geometry']['lng']
    return None, None

def generate_map(lat, lng, location_name):
    my_map = folium.Map(location=[lat, lng], zoom_start=9)
    folium.Marker([lat, lng], popup=location_name).add_to(my_map)
    my_map.save("Location.html")

def main():
    API_KEY = "11e0d6f8fd894f3e872d8aca6500a572"  # Store in an environment variable or config for better security
    phone_number = input("Enter the PhoneNumber with the country code : ")

    location, service_provider = get_location_and_service_provider(phone_number)
    if not location:
        print("Invalid phone number or unable to fetch location.")
        return

    print(f"Location: {location}")
    print(f"Service Provider: {service_provider}")

    lat, lng = get_lat_lng(location, API_KEY)
    if not lat or not lng:
        print("Unable to get latitude and longitude for the location.")
        return

    generate_map(lat, lng, location)

if __name__ == "__main__":
    main()
