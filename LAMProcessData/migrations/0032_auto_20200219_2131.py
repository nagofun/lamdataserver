# Generated by Django 2.2 on 2020-02-19 21:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LAMProcessData', '0031_auto_20200217_1103'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='process_inspect_finedata_discordantrecords',
            name='parameter_realvalue',
        ),
        migrations.AddField(
            model_name='process_inspect_finedata_discordantrecords',
            name='inspect_timestamp',
            field=models.PositiveIntegerField(default=1, unique=True),
            preserve_default=False,
        ),
    ]
