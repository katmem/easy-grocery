# Generated by Django 2.0.7 on 2019-07-30 20:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0094_remove_quantity_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='quantity',
            name='product',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to='shop.OrderItem'),
            preserve_default=False,
        ),
    ]