# Generated by Django 2.0.7 on 2019-08-03 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0122_auto_20190803_1430'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='onSale',
            field=models.BooleanField(default=True),
        ),
    ]
