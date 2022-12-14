# Generated by Django 2.0.7 on 2019-07-29 22:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0086_auto_20190729_2101'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ref_code', models.CharField(max_length=15)),
                ('is_ordered', models.BooleanField(default=False)),
                ('date_ordered', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_ordered', models.BooleanField(default=False)),
                ('date_added', models.DateTimeField(auto_now=True)),
                ('date_ordered', models.DateTimeField(null=True)),
                ('product', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.Products')),
            ],
        ),
        migrations.RemoveField(
            model_name='cart',
            name='products',
        ),
        migrations.RemoveField(
            model_name='cart',
            name='user',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='OrderNum',
        ),
        migrations.AddField(
            model_name='customerswithaccount',
            name='items',
            field=models.ManyToManyField(blank=True, to='shop.Products'),
        ),
        migrations.DeleteModel(
            name='Cart',
        ),
        migrations.DeleteModel(
            name='Payment',
        ),
        migrations.AddField(
            model_name='order',
            name='items',
            field=models.ManyToManyField(to='shop.OrderItem'),
        ),
        migrations.AddField(
            model_name='order',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='shop.CustomersWithAccount'),
        ),
    ]
