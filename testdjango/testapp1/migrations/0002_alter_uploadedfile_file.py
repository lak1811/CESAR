# Generated by Django 3.2.19 on 2023-08-16 00:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testapp1', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uploadedfile',
            name='file',
            field=models.FileField(upload_to='uploads'),
        ),
    ]