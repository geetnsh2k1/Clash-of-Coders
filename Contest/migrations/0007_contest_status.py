# Generated by Django 3.1.3 on 2021-04-22 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Contest', '0006_auto_20210422_1802'),
    ]

    operations = [
        migrations.AddField(
            model_name='contest',
            name='Status',
            field=models.BooleanField(default=True),
        ),
    ]
