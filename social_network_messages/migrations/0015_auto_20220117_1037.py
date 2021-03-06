# Generated by Django 3.2.4 on 2022-01-17 07:37

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('social_network_messages', '0014_auto_20220117_1028'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='coordinates',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='city', to='social_network_messages.city'),
        ),
        migrations.AlterField(
            model_name='message',
            name='createdAt',
            field=models.DateTimeField(default=datetime.datetime(2022, 1, 17, 10, 37, 41, 365057)),
        ),
    ]
