# Generated by Django 2.2 on 2020-04-04 23:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LAMProcessData', '0062_auto_20200404_2203'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lamprocessmission',
            name='LAM_product',
        ),
        migrations.AddField(
            model_name='lamprocessmission',
            name='LAM_product',
            field=models.ManyToManyField(to='LAMProcessData.LAMProduct'),
        ),
    ]
