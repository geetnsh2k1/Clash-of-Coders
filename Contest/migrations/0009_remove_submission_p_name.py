# Generated by Django 3.1.3 on 2021-04-23 07:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Contest', '0008_auto_20210423_1300'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='submission',
            name='P_Name',
        ),
    ]