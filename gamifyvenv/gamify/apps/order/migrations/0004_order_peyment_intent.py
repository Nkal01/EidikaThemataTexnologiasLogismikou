# Generated by Django 5.0 on 2024-02-26 01:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_rename_usermame_order_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='peyment_intent',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
