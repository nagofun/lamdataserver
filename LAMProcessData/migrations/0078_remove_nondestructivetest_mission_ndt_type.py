# Generated by Django 2.2 on 2020-05-05 23:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('LAMProcessData', '0077_auto_20200505_1912'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='nondestructivetest_mission',
            name='NDT_type',
        ),
    ]