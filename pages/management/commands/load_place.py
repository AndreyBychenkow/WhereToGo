import json
import requests

from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from pages.models import Location, LocationImage


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('url', type=str)

    def handle(self, *args, **kwargs):
        url = kwargs['url']
        self.stdout.write(self.style.SUCCESS(
            f'Начало загрузки JSON данных с адреса: {url}'))

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            self.stdout.write(self.style.SUCCESS(
                'JSON файл успешно загружен.'))
        except (requests.RequestException, json.JSONDecodeError) as e:
            self.stderr.write(self.style.ERROR(f'Ошибка: {e}'))
            return

        if isinstance(data, dict):
            data = [data]

        for item in data:
            if not isinstance(item, dict):
                self.stderr.write(self.style.ERROR(
                    'Элемент JSON данных не является словарём'))
                continue

            title = item.get('title')
            if not title:
                self.stderr.write(self.style.ERROR(
                    'Отсутствует поле "title" в JSON данных'))
                continue

            coordinates = item.get('coordinates', {})
            latitude = coordinates.get('lat')
            longitude = coordinates.get('lng')

            if latitude is None or longitude is None:
                self.stderr.write(self.style.ERROR(
                    f'Отсутствуют координаты для места: {title}'))
                continue

            location, _ = Location.objects.get_or_create(
                title=title,
                defaults={
                    'latitude': latitude,
                    'longitude': longitude,
                    'description_short': item.get('description_short', ''),
                    'description_long': item.get('description_long', ''),
                }
            )

            for img_url in item.get('imgs', []):
                self.download_image(img_url, location)

            self.stdout.write(self.style.SUCCESS(
                f'Успешно загружено место: {title}'))

        self.stdout.write(self.style.SUCCESS('Скрипт отработал успешно!'))

    def download_image(self, img_url, location):
        try:
            img_response = requests.get(img_url, timeout=10)
            img_response.raise_for_status()
            image_file = ContentFile(img_response.content)
            location_image = LocationImage(location=location)
            location_image.image.save(img_url.split('/')[-1], image_file)
        except requests.RequestException as e:
            self.stderr.write(self.style.ERROR(
                f'Не удалось загрузить изображение: {img_url}, ошибка: {e}'))
