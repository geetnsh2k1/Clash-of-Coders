# Generated by Django 3.1.3 on 2021-04-23 08:19

import Contest.models
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Contest', '0010_auto_20210423_1322'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contest',
            name='Problem',
            field=models.FileField(upload_to=Contest.models.problem_file_path, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf']), django.core.validators.FileExtensionValidator(allowed_extensions=['docx']), django.core.validators.FileExtensionValidator(allowed_extensions=['txt'])]),
        ),
    ]
