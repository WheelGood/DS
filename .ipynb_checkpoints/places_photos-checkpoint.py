import requests

def get_place_ids(APIkey, lat=47.602150, lon=-122.325971, radius='3000'):
    #this function will not work unless you have a global APIkey
    #these defaults will search the seattle area
    #nearby places search only returns one image, we need more than that so theres an intermediary function to run
    locationbias=f'{radius}@{lat},{lon}'
    url = f'https://maps.googleapis.com/maps/api/place/nearbysearch/json?key={APIkey}&location={lat},{lon}&radius={radius}'
    r = requests.get(url).json()
    places=[]
    for place in r['results']:
        places.append(place['place_id'])
    return places

def get_photo_references(APIkey, places_ids):
    #this takes a list of place IDs and uses the details api to get out up to ten pictures of each
    #places_ids is a list of place id's to get places from
    places_references = {}
    for i, place in enumerate(places_ids):
        url = f'https://maps.googleapis.com/maps/api/place/details/json?key={APIkey}&place_id={place}&fields=photo'
        r = requests.get(url).json()['result']['photos']
        photos = []
        for photo in r:
            photos.append(photo['photo_reference'])
        places_references[place] = photos
    return places_references

def get_photos(APIkey, places_references):
    #this function will not work unless you have a global APIkey
    #places_reference is a dictionary of place_id:[photo_references]
    place_photos = {}
    for place_id, photos in places_references.items():
        pics=[]
        for photo_ref in photos:
            url = f'https://maps.googleapis.com/maps/api/place/photo?key={APIkey}&photoreference={photo_ref}&maxwidth=400'
            r = requests.get(url).content
            pics.append(r)
        place_photos[place_id] = pics
    return place_photos

def get_images(APIkey, lat=47.602150, lon=-122.325971, radius='3000'):
    # this is a pipeline style function that just runs all three of the previous functions
    places = get_place_ids(APIkey, lat, lon, radius)
    places_reference = get_photo_references(APIkey, places)
    photos = get_photos(APIkey, places_reference)
    
    return photos