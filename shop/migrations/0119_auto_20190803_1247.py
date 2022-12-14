# Generated by Django 2.0.7 on 2019-08-03 12:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0118_auto_20190803_1243'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='saleId',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.Sales'),
        ),
        migrations.AlterField(
            model_name='products',
            name='salePrice',
            field=models.DecimalField(decimal_places=2, max_digits=4, null=True),
        ),
    ]
