# Generated by Django 3.2.4 on 2021-12-29 14:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('social_network_messages', '0009_auto_20211229_1738'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='coordinates',
            field=models.ForeignKey(default=9999, on_delete=django.db.models.deletion.PROTECT, related_name='city', to='social_network_messages.city'),
        ),
    ]
