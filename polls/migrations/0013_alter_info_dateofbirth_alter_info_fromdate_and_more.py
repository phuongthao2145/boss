# Generated by Django 4.0.3 on 2022-03-15 03:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0012_alter_info_identity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='info',
            name='DateOfBirth',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='info',
            name='fromDate',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='info',
            name='toDate',
            field=models.DateField(null=True),
        ),
    ]
