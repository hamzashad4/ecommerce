# Generated by Django 5.1 on 2024-10-09 11:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerceapp', '0012_deal_is_active'),
    ]

    operations = [
        migrations.RenameField(
            model_name='deal',
            old_name='deal_ame',
            new_name='deal_name',
        ),
    ]
