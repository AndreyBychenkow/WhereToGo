import json
import time
import requests

from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from django.db import IntegrityError
from django.core.exceptions import MultipleObjectsReturned
from pages.models import Location, LocationImage


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('url', type=str)

    def handle(self, *args, **kwargs):
        url = kwargs['url']
        self.stdout.write(
            self.style.SUCCESS(f'Загрузка JSON данных с {url}')
        )

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            places = response.json()

            if isinstance(places, dict):
                places = [places]

            if not all(isinstance(item, dict) for item in places):
                raise ValueError('Некорректный формат JSON данных')
        except (
                requests.RequestException, json.JSONDecodeError, ValueError
        ) as e:
            self.stderr.write(self.style.ERROR(f'Ошибка: {e}'))
            return

        for item in places:
            title = item.get('title')
            coordinates = item.get('coordinates', {})
            latitude = coordinates.get('lat')
            longitude = coordinates.get('lng')

            if not title or latitude is None or longitude is None:
                self.stderr.write(
                    self.style.ERROR(
                        f'Пропущены обязательные данные в JSON: {item}'
                    )
                )
                continue

            try:
                location, _ = Location.objects.get_or_create(
                    title=title,
                    defaults={
                        'latitude': latitude,
                        'longitude': longitude,
                        'short_description': item.get('short_description', ''),
                        'long_description': item.get('long_description', ''),
                    },
                )
            except MultipleObjectsReturned:
                self.stderr.write(
                    self.style.ERROR(f'Дубликаты мест: "{title}"')
                )
                continue
            except IntegrityError:
                self.stderr.write(
                    self.style.ERROR(f'Ошибка сохранения места: "{title}"')
                )
                continue

            for img_url in item.get('imgs', []):
                attempt = 0
                while attempt < 3:
                    try:
                        img_response = requests.get(img_url, timeout=10)
                        img_response.raise_for_status()
                        image_content = img_response.content

                        LocationImage.objects.create(
                            location=location,
                            image=ContentFile(
                                image_content,
                                name=img_url.split('/')[-1],
                            ),
                        )
                        break
                    except requests.exceptions.HTTPError as e:
                        self.stderr.write(
                            self.style.ERROR(
                                f'Ошибка HTTP при загрузке {img_url}: {e}'
                            )
                        )
                        break
                    except requests.exceptions.ConnectionError as e:
                        self.stderr.write(
                            self.style.ERROR(
                                f'Проблема соединения {img_url}, попытка '
                                f'{attempt + 1}: {e}'
                            )
                        )
                        attempt += 1
                        time.sleep(5)
                    except requests.RequestException as e:
                        self.stderr.write(
                            self.style.ERROR(
                                f'Ошибка при загрузке изображения {img_url}: {e}'
                            )
                        )
                        break

            self.stdout.write(
                self.style.SUCCESS(f'Добавлено место: {title}')
            )

        self.stdout.write(self.style.SUCCESS('Готово!'))
