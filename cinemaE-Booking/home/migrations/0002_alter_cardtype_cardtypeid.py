# Generated by Django 4.0.3 on 2022-03-28 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cardtype',
            name='cardTypeID',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
