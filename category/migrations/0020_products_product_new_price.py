# Generated by Django 2.2.12 on 2021-12-13 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0019_coupon_expiredcoupon'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='product_new_price',
            field=models.IntegerField(null=True),
        ),
    ]
