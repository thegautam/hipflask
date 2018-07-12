''' Module to help with location parsing '''
import re

import googlemaps

KEY = 'AIzaSyD7W7v5psM8TDJwUV2WxsPkoYRtByh07Y0'
gmaps = googlemaps.Client(key=KEY)

stopwords_re = re.compile(r'\b(weather|in|what|is|the)\b', flags=re.IGNORECASE)


class Location:
    '''
    Main location class that converts a string to a
    structured location
    '''
    def __init__(self, text):
        self.lat = None
        self.lng = None
        self.locality_short = None
        self.locality_long = None
        self.postal_code = None
        self.parsed = False

        # Geocode the text using the API
        try:
            geocoded = gmaps.geocode(self._clean(text))
        except:
            geocoded = None

        # Parse out the right fields
        if not geocoded or len(geocoded) < 1:
            return

        self.lat = geocoded[0]['geometry']['location']['lat']
        self.lng = geocoded[0]['geometry']['location']['lng']

        for component in geocoded[0]['address_components']:
            if 'locality' in component['types']:
                self.locality_short = component['short_name']
                self.locality_long = component['long_name']
                # Set parsed only if we found a city
                self.parsed = True
            if 'postal_code' in component['types']:
                self.postal_code = component['short_name']

    def _clean(self, text):
        '''
        Simple heuristics to remove junk words.
        This can be made much better by using NLP/NER techniques
        '''
        return re.sub(stopwords_re, '', text)
