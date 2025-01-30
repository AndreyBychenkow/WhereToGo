import json
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.http import JsonResponse
from .models import Location


def create_feature(location):
    return {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [location.longitude, location.latitude],
        },
        "properties": {
            "title": location.title,
            "placeId": location.id,
            "detailsUrl": reverse('get_location', args=[location.id]),
        },
    }


def show_phones(request):
    locations = Location.objects.prefetch_related('images').all()
    dynamic_features = [create_feature(location) for location in locations]

    geojson_data = {
        "type": "FeatureCollection",
        "features": dynamic_features,
    }

    return render(request, 'index.html', {'geojson_data': geojson_data})


def get_location(request, location_id):
    location = get_object_or_404(
        Location.objects.prefetch_related('images'),
        id=location_id
    )
    images = location.images.all()

    response_json = {
        "title": location.title,
        "imgs": [image.image.url for image in images],
        "description_short": location.short_description,
        "description_long": location.long_description,
        "coordinates": {
            "lat": location.latitude,
            "lng": location.longitude,
        },
    }

    return JsonResponse(
        response_json,
        json_dumps_params={'ensure_ascii': False, 'indent': 4}
    )
