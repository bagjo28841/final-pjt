# Generated by Django 3.1.7 on 2021-05-24 01:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_stamp'),
    ]

    operations = [
        migrations.AddField(
            model_name='stamp',
            name='counter',
            field=models.IntegerField(default=0),
        ),
    ]
