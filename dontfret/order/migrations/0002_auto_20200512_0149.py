# Generated by Django 3.0.5 on 2020-05-12 00:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='total',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Order Total (£)'),
        ),
        migrations.AlterField(
            model_name='orderline',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Price (£)'),
        ),
    ]
