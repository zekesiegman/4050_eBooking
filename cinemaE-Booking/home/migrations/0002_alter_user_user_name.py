# Generated by Django 4.0.3 on 2022-04-14 23:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_name',
            field=models.CharField(max_length=150, unique=True),
        ),
    ]
