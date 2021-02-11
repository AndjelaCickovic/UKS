# Generated by Django 3.1.5 on 2021-02-08 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('issues_app', '0016_auto_20210208_1347'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='comment',
            field=models.CharField(blank=True, max_length=264, null=True),
        ),
        migrations.AlterField(
            model_name='issue',
            name='labels',
            field=models.ManyToManyField(blank=True, null=True, to='issues_app.Label'),
        ),
    ]