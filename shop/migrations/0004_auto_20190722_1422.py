# Generated by Django 2.0.7 on 2019-07-22 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_auto_20190721_1324'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='Barcode',
            field=models.CharField(choices=[('Μανάβικο', 'Μανάβικο'), ('Κρεοπωλείο', 'Κρεοπωλείο'), ('Γαλακτοκομικά-Είδη Ψυγείου', 'Γαλακτοκομικά-Είδη Ψυγείου')], max_length=12),
        ),
    ]
