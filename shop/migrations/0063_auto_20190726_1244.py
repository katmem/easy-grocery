# Generated by Django 2.0.7 on 2019-07-26 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0062_auto_20190725_2132'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
