# Generated by Django 4.2.6 on 2025-01-25 15:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0004_location_description_long_location_description_short'),
    ]

    operations = [
        migrations.AlterField(
            model_name='locationimage',
            name='location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='images', to='pages.location', verbose_name='Связанная локация'),
        ),
    ]
