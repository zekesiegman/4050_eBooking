# Generated by Django 4.0.3 on 2022-04-13 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_promotion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='promotion',
            name='amount',
            field=models.IntegerField(),
        ),
    ]
