# Generated by Django 4.0.3 on 2022-03-27 22:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CardType',
            fields=[
                ('cardTypeID', models.IntegerField(default=1, primary_key=True, serialize=False)),
                ('type', models.CharField(max_length=45)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('userId', models.IntegerField(default=1, primary_key=True, serialize=False)),
                ('phone', models.IntegerField(default=20000000000)),
                ('enrollForPromotions', models.BooleanField(null=True)),
                ('userObj', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Account',
            fields=[
                ('accountID', models.AutoField(default=1, primary_key=True, serialize=False)),
                ('carNo', models.IntegerField()),
                ('expirationDate', models.DateField()),
                ('billingAdd', models.CharField(max_length=45)),
                ('type', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='home.cardtype')),
                ('user_userID', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='home.user')),
            ],
        ),
    ]
