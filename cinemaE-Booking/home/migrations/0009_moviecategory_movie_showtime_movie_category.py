# Generated by Django 4.0.3 on 2022-03-30 20:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_movie_showtime'),
    ]

    operations = [
        migrations.CreateModel(
            name='MovieCategory',
            fields=[
                ('categoryID', models.AutoField(primary_key=True, serialize=False)),
                ('category', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='movie',
            name='showtime',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='home.showtime'),
        ),
        migrations.AddField(
            model_name='movie',
            name='category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='home.moviecategory'),
        ),
    ]
