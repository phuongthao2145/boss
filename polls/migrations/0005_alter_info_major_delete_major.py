# Generated by Django 4.0.3 on 2022-03-15 02:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0004_major_rename_email_info_birthofdate_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='info',
            name='major',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.DeleteModel(
            name='Major',
        ),
    ]
