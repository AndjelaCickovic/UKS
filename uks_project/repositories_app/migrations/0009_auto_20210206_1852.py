# Generated by Django 3.1.5 on 2021-02-06 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repositories_app', '0008_auto_20210204_2326'),
    ]

    operations = [
        migrations.AlterField(
            model_name='repositoryuser',
            name='role',
            field=models.CharField(choices=[('Owner', 'Owner'), ('Coowner', 'Coowner'), ('Colaborator', 'Colaborator')], max_length=11),
        ),
    ]