# Generated by Django 4.0 on 2023-08-27 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testapp1', '0007_remove_person_first_name_remove_person_last_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='Full_name',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='person',
            name='Last_Name',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
    ]
