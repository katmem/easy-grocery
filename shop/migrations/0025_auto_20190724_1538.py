# Generated by Django 2.0.7 on 2019-07-24 15:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0024_auto_20190724_1537'),
    ]

    operations = [
        migrations.RenameField(
            model_name='products',
            old_name='SubCategory2',
            new_name='Subcategory2',
        ),
    ]