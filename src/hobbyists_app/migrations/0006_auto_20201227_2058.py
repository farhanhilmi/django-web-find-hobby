# Generated by Django 3.1.4 on 2020-12-27 13:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hobbyists_app', '0005_auto_20201227_2056'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listforum',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='hobbyists_app.listcategory'),
        ),
    ]
