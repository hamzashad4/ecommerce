# Generated by Django 5.1 on 2024-10-09 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerceapp', '0014_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='cost',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='order',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='order',
            name='profit',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]