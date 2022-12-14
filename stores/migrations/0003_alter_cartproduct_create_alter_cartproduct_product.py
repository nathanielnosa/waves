# Generated by Django 4.1.2 on 2022-10-27 10:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stores', '0002_cart_cartproduct'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartproduct',
            name='create',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='cartproduct',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='stores.product'),
        ),
    ]
