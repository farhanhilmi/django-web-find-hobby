# Generated by Django 3.1.4 on 2021-03-13 04:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hobbyists_app', '0009_auto_20210313_0951'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listevent',
            name='image',
            field=models.ImageField(blank=True, default='default-profile.png', null=True, upload_to='images/'),
        ),
    ]