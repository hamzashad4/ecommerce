# Generated by Django 5.1 on 2024-10-09 11:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerceapp', '0009_deal_dealimage'),
    ]

    operations = [
        migrations.RenameField(
            model_name='deal',
            old_name='dealImage',
            new_name='Deal_Image',
        ),
        migrations.RenameField(
            model_name='deal',
            old_name='dealname',
            new_name='deal_ame',
        ),
    ]
