# Generated by Django 5.0 on 2024-02-26 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0004_order_peyment_intent'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_id',
            field=models.CharField(max_length=250, null=True),
        ),
    ]
