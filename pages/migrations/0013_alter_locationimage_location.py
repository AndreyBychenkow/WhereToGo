# Generated by Django 4.2.6 on 2025-01-29 15:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0012_alter_locationimage_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='locationimage',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='pages.location', verbose_name='Связанная локация'),
        ),
    ]
