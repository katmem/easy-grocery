# Generated by Django 2.0.7 on 2019-07-25 12:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0054_remove_products_subcategory2'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='subcategory',
            field=models.ForeignKey(blank=True, max_length=30, null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.Subcategory'),
        ),
    ]
