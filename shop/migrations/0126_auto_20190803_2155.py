# Generated by Django 2.0.7 on 2019-08-03 21:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0125_remove_products_onsale'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='payment',
        ),
        migrations.AlterField(
            model_name='order',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.Customers'),
        ),
    ]
