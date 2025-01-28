import json
import requests
from concurrent.futures import ThreadPoolExecutor
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from pages.models import Location, LocationImage


class Command(BaseCommand):
    help = 'Загружает место из JSON по URL в базу данных, включая изображения.'

    def add_arguments(self, parser):
        parser.add_argument('url', type=str, help='URL на JSON файл с данными о локации')

    def handle(self, *args, **kwargs):
        url = kwargs['url']

        self.stdout.write(self.style.SUCCESS(f'Начало загрузки JSON данных с адреса: {url}'))

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            self.stdout.write(self.style.SUCCESS('JSON файл успешно загружен.'))
        except requests.RequestException as e:
            self.stderr.write(self.style.ERROR(f'Не удалось загрузить JSON данные по URL: {e}'))
            return

        try:
            data = response.json()
        except json.JSONDecodeError:
            self.stderr.write(self.style.ERROR('Некорректный JSON файл'))
            return

        if isinstance(data, dict):
            data = [data]

        if not isinstance(data, list):
            self.stderr.write(self.style.ERROR('JSON данные не являются списком'))
            return

        def process_item(item):
            if not isinstance(item, dict):
                self.stderr.write(self.style.ERROR('Элемент JSON данных не является словарём'))
                return

            title = item.get('title')
            if not title:
                self.stderr.write(self.style.ERROR('Отсутствует поле "title" в JSON данных'))
                return

            place_id = title.replace(" ", "_").lower()
            latitude = item.get('coordinates', {}).get('lat')
            longitude = item.get('coordinates', {}).get('lng')

            if latitude is None or longitude is None:
                self.stderr.write(self.style.ERROR(f'Отсутствуют координаты для места: {title}'))
                return

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

            def download_image(img_url):
                try:
                    img_response = requests.get(img_url, timeout=10)
                    img_response.raise_for_status()
                    image_file = ContentFile(img_response.content)
                    location_image = LocationImage(location=location)
                    location_image.image.save(img_url.split('/')[-1], image_file)
                except requests.RequestException as e:
                    self.stderr.write(self.style.ERROR(f'Не удалось загрузить изображение: {img_url}, ошибка: {e}'))

            with ThreadPoolExecutor() as executor:
                executor.map(download_image, item.get('imgs', []))

            self.stdout.write(self.style.SUCCESS(f'Успешно загружено место: {title}'))

        with ThreadPoolExecutor() as executor:
            executor.map(process_item, data)

        self.stdout.write(self.style.SUCCESS('Скрипт отработал успешно !'))
