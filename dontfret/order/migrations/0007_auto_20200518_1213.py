# Generated by Django 3.0.5 on 2020-05-18 11:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0006_auto_20200517_2333'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='cardCCV',
        ),
        migrations.RemoveField(
            model_name='order',
            name='cardExpiryDate',
        ),
    ]
