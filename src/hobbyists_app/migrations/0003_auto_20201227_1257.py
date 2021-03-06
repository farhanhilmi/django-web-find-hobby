# Generated by Django 3.1.4 on 2020-12-27 05:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hobbyists_app', '0002_remove_listcategory_user_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='listevent',
            name='kuota',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='HadirEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('event_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='hobbyists_app.listevent')),
                ('user_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
