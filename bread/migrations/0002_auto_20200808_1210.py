# Generated by Django 3.1 on 2020-08-08 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bread', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grain',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
