# Generated by Django 2.2 on 2020-03-26 21:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LAMProcessData', '0055_auto_20200326_2150'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pdfimagecode',
            name='imagecode',
            field=models.TextField(null=True),
        ),
        migrations.AlterIndexTogether(
            name='pdfimagecode',
            index_together={('image_width', 'image_height', 'text')},
        ),
    ]
