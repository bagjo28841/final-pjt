# Generated by Django 3.2.1 on 2021-05-20 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_user_user_rank'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_rank',
            field=models.IntegerField(default=1),
        ),
    ]