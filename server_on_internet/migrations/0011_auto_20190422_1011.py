# Generated by Django 2.2 on 2019-04-22 10:11

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server_on_internet', '0010_auto_20190422_0949'),
    ]

    operations = [
        migrations.AlterField(
            model_name='muon',
            name='detection_time',
            field=models.DateTimeField(default=datetime.datetime(2019, 4, 22, 10, 11, 4, 290141), verbose_name='Detection date'),
        ),
        migrations.AlterField(
            model_name='muon',
            name='image',
            field=models.ImageField(default='muons/muon_2019_4_18_14_17_12_650984.webp', upload_to='muons/', verbose_name='Muon image'),
        ),
    ]
