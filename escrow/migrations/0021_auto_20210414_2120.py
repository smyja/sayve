# Generated by Django 3.1.4 on 2021-04-14 20:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('escrow', '0020_auto_20210414_2110'),
    ]

    operations = [
        migrations.RenameField(
            model_name='log',
            old_name='flw_ref',
            new_name='reference',
        ),
    ]
