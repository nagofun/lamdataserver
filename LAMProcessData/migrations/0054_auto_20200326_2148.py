# Generated by Django 2.2 on 2020-03-26 21:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LAMProcessData', '0053_auto_20200326_2147'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pdfimagecode',
            name='imagecode',
            field=models.TextField(max_length=500),
        ),
    ]