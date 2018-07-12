import itertools
import pytest
from hipflask.location import Location

locations = {
    ('SF', (37.7749295, -122.4194155)),
    ('Seattle', (47.6062095, -122.3320708)),
    ('San Francisco', (37.7749295, -122.4194155)),
    ('15213', (40.4379259, -79.9556424))
}
messages = ['Weather in {}', 'what is weather in {}', '{} weather']
combos = itertools.product(messages, locations)


@pytest.mark.parametrize('message, location', combos)
def test_location_geocode(message, location):
    text = message.format(location[0])
    geocoded = Location(text)
    assert geocoded.parsed, 'Unable to parse location'
    assert (geocoded.lat, geocoded.lng) == location[1], text
    names = [geocoded.locality_short, geocoded.locality_long, geocoded.postal_code]
    assert location[0] in names


@pytest.mark.parametrize('location', ['weather', '', 'weather in akdlfjadslkfajddkj'])
def test_bad_locations(location):
    geocoded = Location(location)
    assert not geocoded.parsed, 'Able to parse bad location'
