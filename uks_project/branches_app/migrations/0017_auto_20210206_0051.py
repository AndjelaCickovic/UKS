# Generated by Django 3.1.5 on 2021-02-06 00:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('branches_app', '0016_auto_20210206_0017'),
    ]

    operations = [
        migrations.AlterField(
            model_name='branch',
            name='name',
            field=models.CharField(max_length=264),
        ),
    ]
