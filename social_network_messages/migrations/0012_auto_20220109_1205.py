# Generated by Django 3.2.4 on 2022-01-09 09:05

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social_network_messages', '0011_alter_message_createdat'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='category_type',
            field=models.IntegerField(choices=[(0, 'Not detected'), (1, 'Cash Machine Breakdown'), (2, 'App Breakdown'), (3, 'Telephone Fraud'), (4, 'Cash Machine Fraud')], default=0),
        ),
        migrations.AlterField(
            model_name='message',
            name='createdAt',
            field=models.DateTimeField(default=datetime.datetime(2022, 1, 9, 12, 4, 58, 605247)),
        ),
        migrations.AlterField(
            model_name='message',
            name='problem_type',
            field=models.IntegerField(choices=[(0, 'No problem'), (1, 'Fraud'), (2, 'Breakdown')], default=0),
        ),
    ]