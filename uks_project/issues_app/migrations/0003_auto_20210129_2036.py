# Generated by Django 3.1.5 on 2021-01-29 20:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('issues_app', '0002_auto_20210129_2027'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='status',
            field=models.CharField(choices=[('Open', 'Opened'), ('Closed', 'Closed')], default='Open', max_length=6),
        ),
        migrations.AlterField(
            model_name='milestone',
            name='status',
            field=models.CharField(choices=[('Open', 'Opened'), ('Closed', 'Closed')], default='Open', max_length=6),
        ),
    ]
