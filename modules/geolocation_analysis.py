import requests
import json

def reverse_geolocation(lat, lon):
    """
    https://nominatim.openstreetmap.org/reverse.php?lat=37.97537&lon=23.73638&zoom=18&format=jsonv2
    """
    try:
        url = "https://nominatim.openstreetmap.org/reverse.php?lat=" + str(lat) + "&lon=" + str(lon) + "&zoom=18&format=jsonv2"
        return json.loads(requests.get(url).text)["display_name"]
    except Exception as e:
        print(e)
    

def analyze(account, tweets):
    places = []

    try:
        f = open('results/' + account + '/places.txt', 'w', encoding='utf8')
    except:
        print('[!] Could not open output file!')

    try:
        for t in tweets:
            if "place" in t:
                if t["place"]:
                    places.append(t["place"])
                    place = t["place"]
                    coords = ""
                    if t["coordinates"] and t["coordinates"]["coordinates"]:
                        coords = str(t["coordinates"]["coordinates"][1]) + ", " + str(t["coordinates"]["coordinates"][0]) + " " + reverse_geolocation(t["coordinates"]["coordinates"][1], t["coordinates"]["coordinates"][0])
                        coords = " " + coords

                    print("[" + account + "] " + "Identified tweet at " + place["full_name"] + " (" + place["country_code"] + ")" + coords)
                    try:
                        f.write(t["created_at"] + " - " + place["full_name"] + " (" + place["country_code"] + ")" + coords + "\n")
                    except:
                        print('[!] Unknown encoding in tweet!')
                        continue
        
    except:
        print('[!] Unknown error! Attempting to gracefully stop.')

    finally:
        f.close()