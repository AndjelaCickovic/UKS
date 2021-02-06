# Generated by Django 3.1.5 on 2021-02-04 22:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_remove_appuser_projects'),
        ('repositories_app', '0006_auto_20210204_2129'),
    ]

    operations = [
        migrations.AddField(
            model_name='repository',
            name='members',
            field=models.ManyToManyField(through='repositories_app.RepositoryUser', to='users.AppUser'),
        ),
        migrations.AddField(
            model_name='repositoryuser',
            name='repository',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='repositories_app.repository'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='repositoryuser',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.appuser'),
        ),
    ]