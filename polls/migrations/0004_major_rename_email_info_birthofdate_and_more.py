# Generated by Django 4.0.3 on 2022-03-15 01:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0003_info_address'),
    ]

    operations = [
        migrations.CreateModel(
            name='Major',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('majorName', models.CharField(max_length=200)),
            ],
        ),
        migrations.RenameField(
            model_name='info',
            old_name='email',
            new_name='birthOfDate',
        ),
        migrations.RenameField(
            model_name='info',
            old_name='mssv',
            new_name='gender',
        ),
        migrations.RenameField(
            model_name='info',
            old_name='name',
            new_name='profileID',
        ),
        migrations.AddField(
            model_name='info',
            name='Identity',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='info',
            name='fname',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='info',
            name='fromDate',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='info',
            name='lname',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='info',
            name='toDate',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='info',
            name='address',
            field=models.EmailField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='info',
            name='attachment',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='info',
            name='major',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='major', to='polls.major'),
        ),
    ]
