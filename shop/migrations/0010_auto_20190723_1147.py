# Generated by Django 2.0.7 on 2019-07-23 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0009_auto_20190723_1144'),
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
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='subcategorysecond',
            name='SubNameSecond',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]