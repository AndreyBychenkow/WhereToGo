# Generated by Django 4.2.6 on 2025-01-29 15:38

from django.db import migrations, models
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0010_rename_description_long_location_long_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='long_description',
            field=tinymce.models.HTMLField(blank=True, default='', verbose_name='Полное описание'),
        ),
        migrations.AlterField(
            model_name='location',
            name='short_description',
            field=models.TextField(blank=True, default='', verbose_name='Краткое описание'),
        ),
    ]
