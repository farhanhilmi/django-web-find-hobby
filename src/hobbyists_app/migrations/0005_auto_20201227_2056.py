# Generated by Django 3.1.4 on 2020-12-27 13:56

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('hobbyists_app', '0004_auto_20201227_1718'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listforum',
            name='category',
            field=models.CharField(default=django.utils.timezone.now, max_length=300),
            preserve_default=False,
        ),
    ]
