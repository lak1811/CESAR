# Generated by Django 4.0 on 2023-08-28 03:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testapp1', '0010_alter_education_year_fin_alter_education_year_ini_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='ID',
            field=models.CharField(max_length=200, primary_key=True, serialize=False),
        ),
    ]
