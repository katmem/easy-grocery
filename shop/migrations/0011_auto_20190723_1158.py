# Generated by Django 2.0.7 on 2019-07-23 11:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0010_auto_20190723_1147'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subcategory',
            name='Subcategory2',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='shop.SubcategorySecond'),
        ),
    ]