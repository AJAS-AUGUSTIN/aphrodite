# Generated by Django 2.2.12 on 2021-11-24 05:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0011_auto_20211123_1350'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderitems',
            old_name='grand_total',
            new_name='sub_total',
        ),
        migrations.RemoveField(
            model_name='order',
            name='order_total',
        ),
        migrations.AddField(
            model_name='order',
            name='grand_total',
            field=models.FloatField(null=True),
        ),
    ]
