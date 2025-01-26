import json
import requests
import os
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from pages.models import Location, LocationImage


class Command(BaseCommand):
    help = 'Load places from a JSON file or URL, or from all JSON files in a directory'

    def add_arguments(self, parser):
        parser.add_argument('path', type=str, help='Path to the JSON file, URL, or directory')

    def handle(self, *args, **kwargs):
        path = kwargs['path']

        if os.path.isdir(path):
            json_files = [f for f in os.listdir(path) if f.endswith('.json')]
            for json_file in json_files:
                full_path = os.path.join(path, json_file)
                self.load_data_from_file(full_path)
        elif os.path.isfile(path):
            self.load_data_from_file(path)
        else:
            self.stderr.write(self.style.ERROR(f'Path {path} is not a valid file or directory'))
            return

    def load_data_from_file(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        if isinstance(data, dict):
            data = [data]

        if not isinstance(data, list):
            self.stderr.write(self.style.ERROR('JSON data is not a list'))
            return

        for item in data:
            if not isinstance(item, dict):
                self.stderr.write(self.style.ERROR('Item in JSON data is not a dictionary'))
                continue

            title = item.get('title')
            place_id = item.get('title').replace(" ", "_").lower()
            latitude = item['coordinates'].get('lat')
            longitude = item['coordinates'].get('lng')
            description_short = item.get('description_short', '')
            description_long = item.get('description_long', '')

            location, created = Location.objects.get_or_create(
                title=title,
                place_id=place_id,
                defaults={
                    'latitude': latitude,
                    'longitude': longitude,
                    'description_short': description_short,
                    'description_long': description_long,
                }
            )

            for img_url in item.get('imgs', []):
                img_response = requests.get(img_url)
                if img_response.status_code == 200:
                    image_file = ContentFile(img_response.content)
                    location_image = LocationImage(location=location)
                    location_image.image.save(img_url.split('/')[-1], image_file)

            self.stdout.write(self.style.SUCCESS(f'Successfully loaded location: {title}'))
