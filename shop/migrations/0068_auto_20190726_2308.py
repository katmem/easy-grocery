# Generated by Django 2.0.7 on 2019-07-26 23:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0067_auto_20190726_2306'),
    ]

    operations = [
        migrations.RenameField(
            model_name='products',
            old_name='Νame',
            new_name='name',
        ),
    ]
