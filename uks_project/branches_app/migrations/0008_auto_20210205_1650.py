# Generated by Django 3.1.5 on 2021-02-05 16:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('repositories_app', '0008_auto_20210204_2326'),
        ('branches_app', '0007_auto_20210205_1649'),
    ]

    operations = [
        migrations.AddField(
            model_name='branch',
            name='commits',
            field=models.ManyToManyField(blank=True, default=None, related_name='commits', to='branches_app.Commit'),
        ),
        migrations.AddField(
            model_name='branch',
            name='name',
            field=models.CharField(blank=True, max_length=264, null=True),
        ),
        migrations.AddField(
            model_name='branch',
            name='parent_branch',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='branches_app.branch'),
        ),
        migrations.AddField(
            model_name='branch',
            name='repository',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='repositories_app.repository'),
        ),
    ]
