# Generated by Django 2.0.7 on 2019-07-25 12:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0052_auto_20190725_1129'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subcategory2',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('SubName2', models.CharField(max_length=255)),
            ],
        ),
        migrations.RemoveField(
            model_name='address',
            name='city',
        ),
        migrations.RemoveField(
            model_name='address',
            name='country',
        ),
        migrations.RemoveField(
            model_name='city',
            name='country',
        ),
        migrations.RenameField(
            model_name='subcategory',
            old_name='CatName',
            new_name='category',
        ),
        migrations.AlterField(
            model_name='products',
            name='subcategory',
            field=models.ForeignKey(max_length=30, null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.Subcategory'),
        ),
        migrations.DeleteModel(
            name='Address',
        ),
        migrations.DeleteModel(
            name='City',
        ),
        migrations.DeleteModel(
            name='Country',
        ),
        migrations.AddField(
            model_name='subcategory2',
            name='SubName',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.Subcategory'),
        ),
        migrations.AddField(
            model_name='products',
            name='Subcategory2',
            field=models.ForeignKey(max_length=30, null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.Subcategory2'),
        ),
    ]