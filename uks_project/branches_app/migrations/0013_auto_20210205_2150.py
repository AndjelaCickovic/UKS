# Generated by Django 3.1.5 on 2021-02-05 21:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('repositories_app', '0008_auto_20210204_2326'),
        ('branches_app', '0012_auto_20210205_1737'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='branch',
            unique_together={('name', 'repository')},
        ),
    ]