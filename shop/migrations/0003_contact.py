# Generated by Django 2.1 on 2019-03-27 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_auto_20190327_2044'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(blank=True, max_length=255)),
                ('address', models.CharField(blank=True, max_length=255)),
                ('email', models.EmailField(blank=True, max_length=255)),
                ('phone_number', models.CharField(blank=True, max_length=255)),
                ('message', models.TextField(blank=True)),
            ],
        ),
    ]
