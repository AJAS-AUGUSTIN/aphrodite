# Generated by Django 2.2.12 on 2021-12-01 08:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0010_auto_20211201_0706'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='categories',
            name='thumbnail',
        ),
    ]