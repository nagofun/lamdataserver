# Generated by Django 2.2 on 2020-03-26 21:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LAMProcessData', '0052_auto_20200326_2145'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pdfimagecode',
            name='imagecode',
            field=models.TextField(),
        ),
    ]