# Generated by Django 3.1.5 on 2021-02-01 20:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('issues_app', '0006_auto_20210201_1948'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='issue',
            name='milestones',
        ),
        migrations.AddField(
            model_name='issue',
            name='milestone',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='milestone', to='issues_app.milestone'),
        ),
    ]
