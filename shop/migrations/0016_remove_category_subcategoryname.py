# Generated by Django 2.0.7 on 2019-07-23 12:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0015_auto_20190723_1210'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='SubcategoryName',
        ),
    ]
