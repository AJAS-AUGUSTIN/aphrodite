# Generated by Django 2.2.12 on 2021-12-22 11:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0021_brand'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brand',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='products',
            name='brand',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='category.Brand'),
        ),
    ]
