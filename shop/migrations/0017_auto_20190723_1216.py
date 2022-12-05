# Generated by Django 2.0.7 on 2019-07-23 12:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0016_remove_category_subcategoryname'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subcategory',
            name='Subcategory2',
        ),
        migrations.AddField(
            model_name='subcategory',
            name='ParentCategory',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to='shop.Category'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='subcategorysecond',
            name='ParentSubCategory',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to='shop.Subcategory'),
            preserve_default=False,
        ),
    ]
