# Generated by Django 3.2.1 on 2021-05-20 07:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0002_auto_20210520_1646'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='movie_id',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
