# Generated by Django 2.0.7 on 2019-08-04 14:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0130_auto_20190804_1216'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Payment',
        ),
        migrations.AlterField(
            model_name='order',
            name='paymentmethod',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to='shop.PaymentMethod'),
            preserve_default=False,
        ),
    ]
