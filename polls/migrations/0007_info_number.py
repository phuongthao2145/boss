# Generated by Django 4.0.3 on 2022-03-15 02:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0006_info_majorid'),
    ]

    operations = [
        migrations.AddField(
            model_name='info',
            name='number',
            field=models.IntegerField(null=True),
        ),
    ]