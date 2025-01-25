import json
from django.shortcuts import render
from .models import Location
from django.http import HttpResponse
from django.shortcuts import get_object_or_404


def create_feature(location):
    return {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [location.latitude, location.longitude],
        },
        "properties": {
            "title": location.title,
            "placeId": location.place_id,
            "detailsUrl": "/static/places/{}.json".format(location.place_id),
        },
    }


def show_phones(request):
    locations = Location.objects.all()
    dynamic_features = [create_feature(location) for location in locations]

    geojson_data = {
        "type": "FeatureCollection",
        "features": dynamic_features,
    }

    return render(request, 'index.html', {'geojson_data': json.dumps(geojson_data)})


def get_location(request,location_id):
    location = get_object_or_404(Location, id=location_id)

    return HttpResponse(location.title)
