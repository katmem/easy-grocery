# Generated by Django 2.0.7 on 2019-07-23 12:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0018_category_parent'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subcategory',
            name='ParentCategory',
        ),
        migrations.RemoveField(
            model_name='subcategorysecond',
            name='ParentSubCategory',
        ),
        migrations.RemoveField(
            model_name='products',
            name='SubCategory2',
        ),
        migrations.RemoveField(
            model_name='products',
            name='Subcategory',
        ),
        migrations.DeleteModel(
            name='Subcategory',
        ),
        migrations.DeleteModel(
            name='SubcategorySecond',
        ),
    ]
