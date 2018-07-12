This is a barebones implementation of the Hipmunk coding challenge.

### Running the Server

```
pip install -r requirements.txt
export FLASK_APP=app.py
flask run -p 9000
```

### Testing

```
pytest .
```

### Outside Sources

* Client for Google Geocoding API
https://github.com/googlemaps/google-maps-services-python

* Client for DarkSky API
https://github.com/ZeevG/python-forecast.io

### Improvements

There is a lot of room for improvement and here are some ideas in no particular order

* Better identification of location in message by using NER techniques. Currently, I'm removing some obvious stopwords and letting Google API do the rest.
* Better identification of intent class with a trained model. Currently, I'm just looking for keywords
* Calling weather & location API asynchronously.
* Unit tests call an external API instead of relying on local results.
* Directory structure & imports could use some cleaning up.
* More robust error checking for bad input, missing data, etc.