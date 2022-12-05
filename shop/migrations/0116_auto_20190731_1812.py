# Generated by Django 2.0.7 on 2019-07-31 18:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0115_quantity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='items',
        ),
        migrations.AddField(
            model_name='order',
            name='items',
            field=models.ManyToManyField(through='shop.Quantity', to='shop.OrderItem'),
        ),
    ]
