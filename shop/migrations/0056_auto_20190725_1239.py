# Generated by Django 2.0.7 on 2019-07-25 12:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0055_auto_20190725_1233'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='Subcategory2',
            field=models.ForeignKey(max_length=30, null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.Subcategory2'),
        ),
        migrations.AlterField(
            model_name='products',
            name='subcategory',
            field=models.ForeignKey(max_length=30, null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.Subcategory'),
        ),
    ]
