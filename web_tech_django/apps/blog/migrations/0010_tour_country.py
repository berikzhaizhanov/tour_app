# Generated by Django 4.1 on 2023-01-20 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_reservation'),
    ]

    operations = [
        migrations.AddField(
            model_name='tour',
            name='country',
            field=models.CharField(blank=True, max_length=60, null=True, verbose_name='Страна'),
        ),
    ]
