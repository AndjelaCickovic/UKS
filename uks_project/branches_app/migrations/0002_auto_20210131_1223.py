# Generated by Django 3.1.5 on 2021-01-31 12:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('branches_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='branch',
            name='parent_branch',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='branches_app.branch'),
        ),
    ]