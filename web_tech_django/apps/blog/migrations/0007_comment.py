# Generated by Django 4.1 on 2023-01-20 08:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_hotel_orderhotel'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
                ('email', models.EmailField(max_length=254)),
                ('description', models.TextField()),
                ('tour_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.tour')),
            ],
        ),
    ]