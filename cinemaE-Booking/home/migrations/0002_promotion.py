# Generated by Django 4.0.3 on 2022-04-13 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Promotion',
            fields=[
                ('promoID', models.AutoField(primary_key=True, serialize=False)),
                ('amount', models.IntegerField(max_length=5)),
                ('valid_thru', models.DateField()),
            ],
        ),
    ]
