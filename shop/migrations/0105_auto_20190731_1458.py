# Generated by Django 2.0.7 on 2019-07-31 14:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0104_customerswithoutaccount_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quantity',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.OrderItem'),
        ),
        migrations.AlterField(
            model_name='quantity',
            name='ref_code',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.Order'),
        ),
    ]
