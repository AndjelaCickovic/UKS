# Generated by Django 3.1.5 on 2021-02-04 13:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects_app', '0003_auto_20210131_1956'),
        ('repositories_app', '0004_auto_20210204_1315'),
        ('issues_app', '0010_merge_20210204_1033'),
    ]

    operations = [
        migrations.AddField(
            model_name='issue',
            name='repository',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='repositories_app.repository'),
        ),
        migrations.AddField(
            model_name='label',
            name='repository',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='repositories_app.repository'),
        ),
        migrations.AddField(
            model_name='milestone',
            name='repository',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='repositories_app.repository'),
        ),
        migrations.AlterField(
            model_name='issue',
            name='column',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='column', to='projects_app.column'),
        ),
    ]
