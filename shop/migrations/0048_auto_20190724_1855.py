# Generated by Django 2.0.7 on 2019-07-24 18:55

from django.db import migrations
import django.db.models.deletion
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0047_auto_20190724_1854'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='subcategory',
            field=smart_selects.db_fields.ChainedForeignKey(chained_field='category', chained_model_field='CatName', on_delete=django.db.models.deletion.CASCADE, to='shop.Subcategory'),
        ),
    ]
