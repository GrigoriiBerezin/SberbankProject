# Generated by Django 3.2.4 on 2021-12-29 14:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('social_network_messages', '0008_alter_message_coordinates'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='city',
            options={'ordering': ['name'], 'verbose_name_plural': 'cities'},
        ),
        migrations.AlterModelOptions(
            name='message',
            options={'ordering': ['createdAt']},
        ),
        migrations.AlterField(
            model_name='message',
            name='coordinates',
            field=models.ForeignKey(default=9999, on_delete=django.db.models.deletion.PROTECT, to='social_network_messages.city'),
        ),
    ]
