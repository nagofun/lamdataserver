# Generated by Django 2.2 on 2020-02-19 22:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LAMProcessData', '0032_auto_20200219_2131'),
    ]

    operations = [
        migrations.AlterField(
            model_name='process_inspect_finedata_discordantrecords',
            name='inspect_timestamp',
            field=models.PositiveIntegerField(),
        ),
    ]
