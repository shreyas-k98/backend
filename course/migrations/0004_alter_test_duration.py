# Generated by Django 4.1.2 on 2022-10-27 03:46

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0003_alter_test_duration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='test',
            name='duration',
            field=models.TimeField(default=datetime.datetime(2022, 10, 27, 3, 46, 14, 481318, tzinfo=datetime.timezone.utc)),
        ),
    ]
