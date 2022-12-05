# Generated by Django 2.0.7 on 2019-07-29 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0079_auto_20190729_1116'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='Address',
        ),
        migrations.RemoveField(
            model_name='cart',
            name='AddressNum',
        ),
        migrations.RemoveField(
            model_name='cart',
            name='Country',
        ),
        migrations.RemoveField(
            model_name='cart',
            name='County',
        ),
        migrations.RemoveField(
            model_name='cart',
            name='Delivered',
        ),
        migrations.RemoveField(
            model_name='cart',
            name='DeliveryTime',
        ),
        migrations.RemoveField(
            model_name='cart',
            name='OrderNum',
        ),
        migrations.RemoveField(
            model_name='cart',
            name='Postcode',
        ),
        migrations.RemoveField(
            model_name='cart',
            name='Region',
        ),
        migrations.AddField(
            model_name='cart',
            name='id',
            field=models.AutoField(auto_created=True, default='1', primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
    ]