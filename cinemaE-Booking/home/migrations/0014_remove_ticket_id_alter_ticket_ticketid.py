# Generated by Django 4.0.3 on 2022-04-29 20:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0013_ticket_id_alter_ticket_ticketid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticket',
            name='id',
        ),
        migrations.AlterField(
            model_name='ticket',
            name='ticketID',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]
