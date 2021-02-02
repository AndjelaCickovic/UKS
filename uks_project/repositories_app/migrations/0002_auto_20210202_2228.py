# Generated by Django 3.1.5 on 2021-02-02 22:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repositories_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='repository',
            name='is_public',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='repository',
            name='description',
            field=models.CharField(blank=True, max_length=264),
        ),
    ]
