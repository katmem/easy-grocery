# Generated by Django 2.0.7 on 2019-07-23 12:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0013_auto_20190723_1207'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='SubcategoryName',
            field=models.ForeignKey(choices=[('Μανάβικο', 'Μανάβικο'), ('Κρεοπωλείο', 'Κρεοπωλείο'), ('Γαλακτοκομικά-Είδη Ψυγείου', 'Γαλακτοκομικά-Είδη Ψυγείου'), ('Τυροκομικά', 'Τυροκομικά'), ('Αλλαντικά', 'Αλλαντικά'), ('Κατεψυγμένα', 'Κατεψυγμένα')], on_delete=django.db.models.deletion.CASCADE, to='shop.Subcategory'),
        ),
    ]