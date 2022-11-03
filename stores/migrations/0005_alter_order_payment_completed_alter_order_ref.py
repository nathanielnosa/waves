# Generated by Django 4.1.2 on 2022-11-01 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stores', '0004_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='payment_completed',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='ref',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]