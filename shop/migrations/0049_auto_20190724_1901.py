# Generated by Django 2.0.7 on 2019-07-24 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0048_auto_20190724_1855'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=255),
        ),
    ]
