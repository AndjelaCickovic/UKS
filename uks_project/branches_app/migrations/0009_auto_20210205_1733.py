# Generated by Django 3.1.5 on 2021-02-05 17:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('branches_app', '0008_auto_20210205_1650'),
    ]

    operations = [
        migrations.AlterField(
            model_name='branch',
            name='parent_branch',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='branches_app.branch'),
        ),
    ]