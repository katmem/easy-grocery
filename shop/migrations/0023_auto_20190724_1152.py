# Generated by Django 2.0.7 on 2019-07-24 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0022_auto_20190723_1332'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='CatName',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='subcategory',
            name='SubName',
            field=models.CharField(max_length=255),
        ),
    ]