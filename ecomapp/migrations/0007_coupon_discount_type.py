# Generated by Django 4.0.6 on 2023-05-15 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecomapp', '0006_coupon'),
    ]

    operations = [
        migrations.AddField(
            model_name='coupon',
            name='discount_type',
            field=models.CharField(choices=[('Direct', 'Direct'), ('Packed', 'Cash')], default='', max_length=20),
        ),
    ]