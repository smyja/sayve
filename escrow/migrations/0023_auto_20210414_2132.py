# Generated by Django 3.1.4 on 2021-04-14 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('escrow', '0022_auto_20210414_2131'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='narration',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
