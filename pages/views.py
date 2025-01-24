import json
from itertools import chain
from django.shortcuts import render
from .models import Location


def create_feature(coordinates, title, place_id, details_url):
    return {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": coordinates,
        },
        "properties": {
            "title": title,
            "placeId": place_id,
            "detailsUrl": details_url,
        },
    }


def show_phones(request):
    locations = Location.objects.all()

    static_features = [
        create_feature(
            coordinates=[37.62, 55.793676],
            title="«Легенды Москвы»",
            place_id="moscow_legends",
            details_url="/static/places/moscow_legends.json",
        ),
        create_feature(
            coordinates=[37.64, 55.753676],
            title="Крыши24.рф",
            place_id="roofs24",
            details_url="/static/places/roofs24.json",
        ),
    ]

    dynamic_features = [
        create_feature(
            coordinates=[location.longitude, location.latitude],
            title=location.title,
            place_id=location.place_id,
            details_url=location.details_url,
        )
        for location in locations
        if location.longitude and location.latitude
    ]

    geojson_data = {
        "type": "FeatureCollection",
        "features": list(chain(static_features, dynamic_features)),
    }

    return render(request, 'index.html', {'geojson_data': json.dumps(geojson_data)})
