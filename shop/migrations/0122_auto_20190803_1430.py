# Generated by Django 2.0.7 on 2019-08-03 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0121_auto_20190803_1413'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='salePrice',
            field=models.DecimalField(decimal_places=2, max_digits=4),
        ),
    ]
