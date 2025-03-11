import phonenumbers
from phonenumbers import geocoder #geocoder is used to find location of a number
from phonenumbers import carrier  #carrier is used to find network provider of a number
import folium  #Folium is used for creating interactive maps in Python.
from opencage.geocoder import OpenCageGeocode # To represent the phone number on map

key = "c428ac8c58ce441b80e7520744f42055"
number = input("Enter phone number with country code:")

# Number's Location
check_number = phonenumbers.parse(number) #The parse function takes a phone number (as a string) and extracts its components based on a specified region.
number_location = geocoder.description_for_number(check_number,"en") # It convet the number into any language and we use en to convert it into english
print(f"Location Of Number: {number_location}")

# Service provider of your number+

network = carrier.name_for_number(check_number,"en")
print(f"Network of Number: {network} ")

geocoder_map = OpenCageGeocode(key) # To convert into map

query = str(number_location)
results = geocoder_map.geocode(query)
if results:
    lat = results[0]['geometry']['lat']
    lng = results[0]['geometry']['lng']

    location = geocoder_map.reverse_geocode(lat,lng)
    if location:
        print("Full Location Details:", location[0]["components"])  # Debugging

        city = location[0]["components"].get('city') or \
            location[0]["components"].get('town') or \
            location[0]["components"].get('village') or \
            location[0]["components"].get('municipality', 'Not Found')

        state = location[0]["components"].get('state') or \
                location[0]["components"].get('region') or \
                location[0]["components"].get('state_district', 'Not Found')

        print(f"State of Number: {state}")
        print(f"City of Number: {city}")

        if city != 'Not Found':
            city_map = geocoder_map.geocode(city)
            if city_map:  
                city_lat = city_map[0]['geometry']['lat']
                city_lng = city_map[0]['geometry']['lng']
                print(f"City Coordinates: {city_lat}, {city_lng}")
            else:
                print("Could not fetch city coordinates.")
        else:
            print(f"Coordinates: {lat}, {lng}")
    else:
        print('City not Found')

    map_location = folium.Map(location = [lat,lng], zoom_start=9)
    folium.Marker([lat,lng], popup=number_location).add_to(map_location)
    map_location.save('mylocation.html')
else:
    print("Location Does not found!!")
