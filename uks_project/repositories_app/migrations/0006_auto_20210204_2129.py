# Generated by Django 3.1.5 on 2021-02-04 21:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('repositories_app', '0005_merge_20210204_2115'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='repository',
            name='branches',
        ),
        migrations.RemoveField(
            model_name='repository',
            name='projects',
        ),
        migrations.RemoveField(
            model_name='repository',
            name='repository_users',
        ),
        migrations.RemoveField(
            model_name='repository',
            name='wiki',
        ),
    ]