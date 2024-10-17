# Generated by Django 5.1 on 2024-10-11 11:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerceapp', '0016_cartitem_total'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderItems',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cost', models.DecimalField(decimal_places=2, max_digits=10)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('total', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('added_at', models.DateTimeField(auto_now_add=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='ecommerceapp.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecommerceapp.products')),
            ],
        ),
    ]