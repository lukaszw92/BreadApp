# Generated by Django 3.1 on 2020-08-20 13:03

import bread.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bread', '0008_auto_20200819_0935'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bread',
            name='baking_temperature',
            field=models.IntegerField(validators=[bread.models.positive_validator]),
        ),
        migrations.AlterField(
            model_name='bread',
            name='salt',
            field=models.IntegerField(validators=[bread.models.non_negative_validator]),
        ),
        migrations.AlterField(
            model_name='bread',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.user'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='bread',
            name='water',
            field=models.IntegerField(validators=[bread.models.positive_validator]),
        ),
        migrations.AlterField(
            model_name='flour',
            name='type',
            field=models.IntegerField(null=True, validators=[bread.models.non_negative_validator]),
        ),
        migrations.AlterField(
            model_name='flourinbread',
            name='grams',
            field=models.IntegerField(null=True, validators=[bread.models.positive_validator]),
        ),
        migrations.AlterField(
            model_name='flourinleaven',
            name='grams',
            field=models.IntegerField(null=True, validators=[bread.models.positive_validator]),
        ),
        migrations.AlterField(
            model_name='leaven',
            name='sourdough',
            field=models.IntegerField(validators=[bread.models.positive_validator]),
        ),
        migrations.AlterField(
            model_name='leaven',
            name='water',
            field=models.IntegerField(validators=[bread.models.positive_validator]),
        ),
    ]
