# Generated by Django 2.2 on 2020-02-08 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LAMProcessData', '0017_auto_20200207_2245'),
    ]

    operations = [
        migrations.AddField(
            model_name='lamprocessparameters',
            name='available',
            field=models.BooleanField(default=True),
        ),
    ]