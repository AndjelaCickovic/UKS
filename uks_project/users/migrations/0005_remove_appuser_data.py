# Generated by Django 3.1.5 on 2021-02-01 14:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_appuser_data'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appuser',
            name='data',
        ),
    ]
