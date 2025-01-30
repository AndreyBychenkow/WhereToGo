import json
import requests

from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from django.db import IntegrityError, MultipleObjectsReturned
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
            answer_json_data = response.json()
            self.stdout.write(self.style.SUCCESS(
                'JSON файл успешно загружен.'))
        except (requests.RequestException, json.JSONDecodeError) as e:
            self.stderr.write(self.style.ERROR(f'Ошибка: {e}'))
            return

        if isinstance(answer_json_data, dict):
            answer_json_data = [answer_json_data]

        for item in answer_json_data:
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

            try:
                location, created = Location.objects.get_or_create(
                    title=title,
                    defaults={
                        'latitude': latitude,
                        'longitude': longitude,
                        'short_description': item.get('short_description', ''),
                        'long_description': item.get('long_description', ''),
                    }
                )
            except MultipleObjectsReturned:
                self.stderr.write(self.style.ERROR(
                    f'Обнаружено несколько мест с заголовком "{title}".'))
                continue
            except IntegrityError:
                self.stderr.write(self.style.ERROR(
                    f'Ошибка целостности данных при создании места: {title}.'))
                continue

            for img_url in item.get('imgs', []):
                LocationImage.objects.create(
                    location=location,
                    image=ContentFile(requests.get(
                        img_url).content, name=img_url.split('/')[-1])
                )

            self.stdout.write(self.style.SUCCESS(
                f'Успешно загружено место: {title}'))

        self.stdout.write(self.style.SUCCESS('Скрипт отработал успешно!'))
