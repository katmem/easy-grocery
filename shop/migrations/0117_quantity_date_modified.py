# Generated by Django 2.0.7 on 2019-08-01 21:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0116_auto_20190731_1812'),
    ]

    operations = [
        migrations.AddField(
            model_name='quantity',
            name='date_modified',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
