# Generated by Django 5.0.7 on 2024-08-02 09:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chore', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='chore',
            name='frequency',
            field=models.DurationField(choices=[(datetime.timedelta(days=7), 'once in a week'), (datetime.timedelta(days=14), 'once in 2 weeks'), (datetime.timedelta(days=21), 'once in 3 weeks'), (datetime.timedelta(days=28), 'once in a month'), (datetime.timedelta(days=56), 'once in 2 months'), (datetime.timedelta(days=182), 'once in 6 months')], default=datetime.timedelta(days=7)),
        ),
    ]
