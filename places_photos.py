import requests

def get_place_ids(lat=47.602150, lon=-122.325971, radius='3000', kind='store'):
    #this function will not work unless you have a global APIkey
    #these defaults will search the seattle area
    #nearby places search only returns one image, we need more than that so theres an intermediary function to run
    locationbias=f'{radius}@{lat},{lon}'
    url = f'https://maps.googleapis.com/maps/api/place/nearbysearch/json?key={APIkey}&location={lat},{lon}&radius={radius}&type={kind}'
    try:
        r = requests.get(url).json()['results']
        places=[]
        for place in r:
            places.append(place['place_id'])
    except:
        pass
    return places

def get_photo_references(places_ids):
    #this takes a list of place IDs and uses the details api to get out up to ten pictures of each
    #places_ids is a list of place id's to get places from
    places_references = {}
    for i, place in enumerate(places_ids):
        url = f'https://maps.googleapis.com/maps/api/place/details/json?key={APIkey}&place_id={place}&fields=photo'
        try:
            r = requests.get(url).json()['result']['photos']
            photos = []
            for photo in r:
                photos.append(photo['photo_reference'])
            places_references[place] = photos
        except:
            pass
    return places_references

def get_photos(places_references):
    #this function will not work unless you have a global APIkey
    #places_reference is a dictionary of place_id:[photo_references]
    place_photos = {}
    for place_id, photos in places_references.items():
        pics=[]
        for photo_ref in photos:
            url = f'https://maps.googleapis.com/maps/api/place/photo?key={APIkey}&photoreference={photo_ref}&maxwidth=400'
            r = requests.get(url)
            if r.status_code == 200:
                pics.append(r.content)
        place_photos[place_id] = pics
    return place_photos

def get_images(APIkey, lat=47.602150, lon=-122.325971, radius='3000'):
    # this is a pipeline style function that just runs all three of the previous functions
    places = get_place_ids(APIkey, lat, lon, radius)
    places_reference = get_photo_references(APIkey, places)
    photos = get_photos(APIkey, places_reference)
    
    return photos

#this is a generator function because even with just this subset of six kinds it overloaded my computers memory. 
#this generator should be sent through the 'ramp/not ramp' detector, then the ramps get sent through the ramp judger
#the list of KINDS at the end is all the possible kinds that one could search for, theoretically the generator should work with that long list but I haven't tested it yet
def get_lotsa_images(APIkey, lat=47.602150, lon=-122.325971, radius='3000', kinds=['atm','store','restaurant','spa','cafe','parking']):
    places=[]
    for ty in kinds:
        print('Getting place_ids for', ty)
        places += get_place_ids(lat=lat, lon=lon, radius=radius, kind=ty)
        print('Place_ids aquired')
        places_reference = get_photo_references( places)
        print('photo references aquired')
        photos = get_photos(places_reference)
        yield photos

KINDS = ['accounting',
 'airport',
 'amusement_park',
 'aquarium',
 'art_gallery',
 'atm',
 'bakery',
 'bank',
 'bar',
 'beauty_salon',
 'bicycle_store',
 'book_store',
 'bowling_alley',
 'bus_station',
 'cafe',
 'campground',
 'car_dealer',
 'car_rental',
 'car_repair',
 'car_wash',
 'casino',
 'cemetery',
 'church',
 'city_hall',
 'clothing_store',
 'convenience_store',
 'courthouse',
 'dentist',
 'department_store',
 'doctor',
 'drugstore',
 'electrician',
 'electronics_store',
 'embassy',
 'fire_station',
 'florist',
 'funeral_home',
 'furniture_store',
 'gas_station',
 'grocery_or_supermarket',
 'gym',
 'hair_care',
 'hardware_store',
 'hindu_temple',
 'home_goods_store',
 'hospital',
 'insurance_agency',
 'jewelry_store',
 'laundry',
 'lawyer',
 'library',
 'light_rail_station',
 'liquor_store',
 'local_government_office',
 'locksmith',
 'lodging',
 'meal_delivery',
 'meal_takeaway',
 'mosque',
 'movie_rental',
 'movie_theater',
 'moving_company',
 'museum',
 'night_club',
 'painter',
 'park',
 'parking',
 'pet_store',
 'pharmacy',
 'physiotherapist',
 'plumber',
 'police',
 'post_office',
 'primary_school',
 'real_estate_agency',
 'restaurant',
 'roofing_contractor',
 'rv_park',
 'school',
 'secondary_school',
 'shoe_store',
 'shopping_mall',
 'spa',
 'stadium',
 'storage',
 'store',
 'subway_station',
 'supermarket',
 'synagogue',
 'taxi_stand',
 'tourist_attraction',
 'train_station',
 'transit_station',
 'travel_agency',
 'university',
 'veterinary_care',
 'zoo ']