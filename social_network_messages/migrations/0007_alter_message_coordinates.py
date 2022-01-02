# Generated by Django 3.2.4 on 2021-12-29 14:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('social_network_messages', '0006_alter_message_coordinates'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='coordinates',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='social_network_messages.city'),
        ),
    ]