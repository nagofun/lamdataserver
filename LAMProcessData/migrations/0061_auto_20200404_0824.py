# Generated by Django 2.2 on 2020-04-04 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LAMProcessData', '0060_auto_20200328_1638'),
    ]

    operations = [
        migrations.AddField(
            model_name='process_mission_timecut',
            name='finedata_finish_recordid',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='process_mission_timecut',
            name='finedata_start_recordid',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='pdfimagecode',
            name='OriginalImage',
            field=models.ImageField(blank=True, null=True, upload_to='PDFCode/OriginalImage/'),
        ),
    ]
