# Generated by Django 3.1.3 on 2021-04-23 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Contest', '0012_auto_20210423_1701'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='Time',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
