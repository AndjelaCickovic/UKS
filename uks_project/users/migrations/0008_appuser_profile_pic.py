# Generated by Django 3.1.5 on 2021-02-13 22:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_remove_appuser_projects'),
    ]

    operations = [
        migrations.AddField(
            model_name='appuser',
            name='profile_pic',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='profile_pics'),
        ),
    ]
