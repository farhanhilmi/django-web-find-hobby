# Generated by Django 3.1.4 on 2021-03-13 01:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hobbyists_app', '0007_listforum_user_like'),
    ]

    operations = [
        migrations.AddField(
            model_name='listevent',
            name='hadir',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]