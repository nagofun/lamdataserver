# Generated by Django 2.2 on 2019-11-30 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LAMProcessData', '0002_auto_20191130_0047'),
    ]

    operations = [
        migrations.AlterField(
            model_name='oxygendata',
            name='acquisition_time',
            field=models.DateTimeField(),
        ),
    ]