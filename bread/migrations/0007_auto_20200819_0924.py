# Generated by Django 3.1 on 2020-08-19 07:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bread', '0006_auto_20200818_2331'),
    ]

    operations = [
        migrations.AddField(
            model_name='leaven',
            name='grams',
            field=models.IntegerField(default=None),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name='leaven',
            name='flour',
        ),
        migrations.AddField(
            model_name='leaven',
            name='flour',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='bread.flour'),
        ),
        migrations.DeleteModel(
            name='FlourInLeaven',
        ),
    ]
