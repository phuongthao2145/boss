# Generated by Django 4.0.3 on 2022-03-10 01:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='info',
            name='status',
            field=models.IntegerField(default=0),
        ),
    ]